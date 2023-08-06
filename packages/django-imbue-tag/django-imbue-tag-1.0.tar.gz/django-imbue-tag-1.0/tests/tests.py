import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase


class BasicTestCase(TestCase):

    def test_simple_usage(self):
        value = template_file(
            """
            {% load imbue_tag %}

            {
                "value": {% slot %}
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{value}' %}}
                1
            {{% endimbue %}}
            """
        )
        
        result = json.loads(template.render(Context({})))

        self.assertDictEqual(result, {'value': 1})

    def test_imbued_template_name_in_variable(self):
        value = template_file(
            """
            {% load imbue_tag %}

            {
                "value": {% slot %}
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue name %}}
                1
            {{% endimbue %}}
            """
        )

        result = json.loads(template.render(Context({'name': value})))

        self.assertDictEqual(result, {'value': 1})

    def test_context_separation(self):
        """Variables from outer context are not accessible inside imbued template (with the exception of ``csrf_token``) by default."""
        value = template_file(
            """
            {% load imbue_tag %}

            {
                "value": [{% slot %}]
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{value}' %}}
                {{{{ variable }}}}
            {{% endimbue %}}
            """
        )

        result = json.loads(template.render(Context({'variable': 1})))

        self.assertDictEqual(result, {'value': []})

    def test_variable_injection(self):
        value = template_file(
            """
            {% load imbue_tag %}

            {
                "value": [{% slot %}]
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{value}' variable=variable %}}
                {{{{ variable }}}}
            {{% endimbue %}}
            """
        )

        result = json.loads(template.render(Context({'variable': 1})))
        
        self.assertDictEqual(result, {'value': [1]})

    def test_complex_template_syntax(self):
        value = template_file(
            """
            {% load imbue_tag %}

            {
                "value": {% slot %}
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{value}' animals=animals %}}
                [
                    {{% for animal in  animals %}}
                        "{{{{ animal }}}}" {{% if not forloop.last %}},{{% endif %}}
                    {{% endfor %}}
                ]
            {{% endimbue %}}
            """
        )

        result = json.loads(template.render(Context({'animals': ['cat', 'guinea pig']})))

        self.assertDictEqual(result, {'value': ['cat', 'guinea pig']})

    def test_multiple_slot_in_imbued_template(self):
        repeated = template_file(
            """
            {% load imbue_tag %}

            {
                "villain": {% slot %},
                "hero": {% slot %}
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{repeated}' %}}
                true
            {{% endimbue %}}
            """
        )

        result = json.loads(template.render(Context({})))

        self.assertDictEqual(result, {'villain': True, 'hero': True})

    def test_state_separation(self):
        """If slot is repeated, then each should receive copy of injected template so that nodes won't share state."""
        repeated = template_file(
            """
            {% load imbue_tag %}

            {
                "A": [{% slot %}],
                "B": [{% slot %}]
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{repeated}' steps=steps %}}
                {{% for i in steps %}}
                    {{% cycle '1' '2' '3' '4' %}}{{% if not forloop.last %}},{{% endif %}}
                {{% endfor %}}
            {{% endimbue %}}
            """
        )

        result = json.loads(template.render(Context({'steps': [1, 2]})))

        self.assertDictEqual(result, {'A': [1, 2], 'B': [1, 2]})

    def test_slot_inside_loop(self):
        loop = template_file(
            """
            {% load imbue_tag %}

            {
                "values": [
                    {% for i in steps %}
                        {% slot %}{% if not forloop.last %},{% endif %}
                    {% endfor %}
                ]
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{loop}' steps=steps %}}
                {{% cycle '1' '2' '3' '4' %}}
            {{% endimbue %}}
            """
        )

        result = json.loads(template.render(Context({'steps': [1, 2, 3, 4]})))

        self.assertDictEqual(result, {'values': [1, 2, 3, 4]})

    def test_csrf_token_auto_passing(self):
        csrf_token = template_file(
            """
            {
                "csrf_token": "{{ csrf_token }}"
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{csrf_token}' %}}
            {{% endimbue %}}
            """
        )

        result = json.loads(template.render(Context({'csrf_token': "TOKEN"})))

        self.assertDictEqual(result, {'csrf_token': "TOKEN"})

    def test_in_loop(self):
        obj = template_file(
            """
            {% load imbue_tag %}

            {
                "value": {% slot %}
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            [
                {{% for i in steps %}}
                    {{% imbue '{obj}' val=i %}}{{{{ val }}}}{{% endimbue %}}
                    {{% if not forloop.last %}},{{% endif %}}
                {{% endfor %}}
            ]
            """
        )

        result = json.loads(template.render(Context({'steps': [1, 2, 3]})))

        self.assertListEqual(result, [{"value": 1}, {"value": 2}, {"value": 3}])

    def test_not_altering_target_template(self):
        """If DEBUG = True Django django.template.backends.django.DjangoTemplates adds cached.Loader that loads and parsers given template ONCE. 
        After that template object is stored in internal cache and returned each time when loader is asked for it again. 
        Thus it cannot be modified in any way because it may skew rendering.
        """
        immutable = template_file(
            """
            {% load imbue_tag %}

            {
                "value": {% slot %}
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{immutable}' val=1 %}}{{{{ val }}}}{{% endimbue %}}
            """
        )

        template.render(Context({}))

        # Simulating repeated rendering
        # imbue tag should recive "immutable" template from cache
        result = json.loads(template.render(Context({})))

        # If modification occured, then {{ val }} will be placed again and the end result will look like this:
        #        {{ val }}{{ val }}
        # rendering 11 instead of 1
        self.assertDictEqual(result, {"value": 1})

    def test_missing_imbued_template_name(self):
        template_str ="""
        {% load imbue_tag %}

        {% imbue %}
            content
        {% endimbue %}
        """

        self.assertRaisesMessage(
            TemplateSyntaxError, 
            'imbue tag requires a single argument - template name', 
            Template, 
            template_str
        )


class NamedSlotTestCase(TestCase):

    def test_simple_usage(self):
        value = template_file(
            """
            {% load imbue_tag %}

            {
                "value": {% slot "value" %}
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{value}' %}}
                {{% template_for_slot "value" %}}
                    1
                {{% end_template_for_slot %}}
            {{% endimbue %}}
            """
        )
        
        result = json.loads(template.render(Context({})))

        self.assertDictEqual(result, {'value': 1})

    def test_multiple_slots(self):
        multiple = template_file(
            """
            {% load imbue_tag %}

            {
                "A": {% slot "A" %},
                "B": {% slot "B" %}

            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{multiple}' %}}
                {{% template_for_slot "B" %}}
                    2
                {{% end_template_for_slot %}}

                {{% template_for_slot "A" %}}
                    1
                {{% end_template_for_slot %}}
            {{% endimbue %}}
            """
        )

        result = json.loads(template.render(Context({})))

        self.assertDictEqual(result, {'A': 1, 'B': 2})


    def test_mixed_content_in_injected_template(self):
        """``imbue`` content must be single template OR set of ``template_for_slot`` 
        containing templates for named slots in imbued template. Those two types of content cannot be mixed.
        """
        value = template_file(
            """
            {% load imbue_tag %}

            {
                "value": {% slot "value" %}
            }
            """
        )

        template_str = f"""
            {{% load imbue_tag %}}

            {{% imbue '{value}' %}}
                {{% template_for_slot "value" %}}
                    1
                {{% end_template_for_slot %}}

                "{{% lorem %}}"
            {{% endimbue %}}
            """

        self.assertRaisesMessage(
            TemplateSyntaxError,
            'cannot mix named slot templates with normal content',
            Template,
            template_str
        )

        template_str = f"""
            {{% load imbue_tag %}}

            {{% imbue '{value}' %}}
                "{{% lorem %}}"

                {{% template_for_slot "value" %}}
                    1
                {{% end_template_for_slot %}}
            {{% endimbue %}}
            """

        self.assertRaisesMessage(
            TemplateSyntaxError,
            'cannot mix normal content with named slot templates',
            Template,
            template_str
        )

    def test_redeclared_template_for_slot(self):
        value = template_file(
            """
            {% load imbue_tag %}

            {
                "value": {% slot "value" %}
            }
            """
        )

        template_str = f"""
            {{% load imbue_tag %}}

            {{% imbue '{value}' %}}
                {{% template_for_slot "value" %}}
                    1
                {{% end_template_for_slot %}}

                {{% template_for_slot "value" %}}
                    2
                {{% end_template_for_slot %}}
            {{% endimbue %}}
            """

        self.assertRaisesMessage(
            TemplateSyntaxError,
            'redeclared slot template "value"',
            Template,
            template_str
        )

    def test_missing_template_for_slot(self):
        value = template_file(
            """
            {% load imbue_tag %}

            {
                "value": {% slot "value" %}
            }
            """
        )

        template = Template(
            f"""
            {{% load imbue_tag %}}

            {{% imbue '{value}' %}}
                {{% template_for_slot "other" %}}
                    1
                {{% end_template_for_slot %}}
            {{% endimbue %}}
            """
        )

        self.assertRaisesMessage(
            TemplateSyntaxError,
            'could not find template for slot "value"',
            template.render,
            Context({})
        )

    def test_missing_slot_name_in_template_for_slot(self):
        template_str ="""
        {% load imbue_tag %}

        {% imbue %}
            {% template_for_slot %}
            {% end_template_for_slot %}
        {% endimbue %}
        """

        self.assertRaisesMessage(
            TemplateSyntaxError, 
            'template_for_slot tag requires only one positional argument - target slot name', 
            Template, 
            template_str
        )

    def test_multiple_parameters_in_template_for_slot(self):
        template_str ="""
        {% load imbue_tag %}

        {% imbue %}
            {% template_for_slot 'name1' 'name2' %}
            {% end_template_for_slot %}
        {% endimbue %}
        """

        self.assertRaisesMessage(
            TemplateSyntaxError, 
            'template_for_slot tag requires only one positional argument - target slot name', 
            Template, 
            template_str
        )

    def test_non_string_slot_name_in_template_for_slot(self):
        template_str ="""
        {% load imbue_tag %}

        {% imbue %}
            {% template_for_slot variable %}
            {% end_template_for_slot %}
        {% endimbue %}
        """

        self.assertRaisesMessage(
            TemplateSyntaxError, 
            'template_for_slot tag expects explicit string value', 
            Template, 
            template_str
        )

    def test_slot_with_multiple_parameters(self):
        template_str ="""
        {% load imbue_tag %}

        {% slot "name1" "name2" %}
        """

        self.assertRaisesMessage(
            TemplateSyntaxError, 
            'slot tag takes only one optional argument - name', 
            Template, 
            template_str
        )

    def test_non_string_slot_name(self):
        template_str ="""
        {% load imbue_tag %}

        {% slot variable %}
        """

        self.assertRaisesMessage(
            TemplateSyntaxError, 
            'slot tag expects explicit string value', 
            Template, 
            template_str
        )


def template_file(content):
    tmp_file = NamedTemporaryFile(mode='w', dir=settings.TEMPLATE_DIR, delete=False)
    tmp_file.write(content)
    tmp_file.close()
    return Path(tmp_file.name).name 
