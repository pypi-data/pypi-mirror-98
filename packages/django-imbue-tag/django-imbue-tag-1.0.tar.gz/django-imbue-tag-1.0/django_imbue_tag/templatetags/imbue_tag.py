from copy import deepcopy

from django import template
from django.template.base import TextNode
from django.template.library import parse_bits


register = template.Library()

SLOT_TEMPLATES_CTX_VAR = '__INBUE_SLOT_TEMPLATES__'


@register.tag('imbue')
def do_imbue(parser, token):
    nodelist = parser.parse(('endimbue',))

    contents = token.split_contents()
    tag_name, bits = contents[0], contents[1:]
    parser.delete_first_token()

    if len(bits) == 0:
        raise template.TemplateSyntaxError(
            '%s tag requires a single argument - template name' % tag_name
        )

    args, kwargs = parse_bits(
        parser, bits, ('template_name',), None, tuple(), None,
        tuple(), tuple(), False, tag_name
    )


    if SLOT_TEMPLATES_CTX_VAR in kwargs:
        raise template.TemplateSyntaxError(
            '%s tag cannot use %s as context variable name - restricted name for internal use' % (tag_name, SLOT_TEMPLATES_CTX_VAR)
        )

    return ImbueNode(nodelist, args[0], kwargs)


class ImbueNode(template.Node):

    def __init__(self, nodelist, template_name, kwargs):
        self.nodelist = nodelist
        self.template_name = template_name
        self.kwargs = kwargs
        self.slot_templates = self.get_slot_templates()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def render(self, context):
        template_name, resolved_kwargs = self.get_resolved_arguments(context)

        t = context.template.engine.get_template(template_name)
        template_node_list = t.nodelist

        new_context = context.new(resolved_kwargs)
        new_context[SLOT_TEMPLATES_CTX_VAR] = self.slot_templates

        csrf_token = context.get('csrf_token')
        if csrf_token is not None:
            new_context['csrf_token'] = csrf_token

        return template_node_list.render(new_context)

    def get_slot_templates(self):
        templates = {}
        if self.nodelist:
            first_node_index = self.get_first_meaningful_node_index()
            if first_node_index < len(self.nodelist):
                if type(self.nodelist[first_node_index]) is TemplateForSlot:
                    for node in self.nodelist[first_node_index:]:
                        if self.is_empty_text_node(node):
                            continue

                        if type(node) is not TemplateForSlot:
                            raise template.TemplateSyntaxError('cannot mix named slot templates with normal content')
                        if node.target_slot_name in templates:
                            raise template.TemplateSyntaxError('redeclared slot template "%s"' % node.target_slot_name)

                        templates[node.target_slot_name] = node.nodelist
                else:
                    for node in self.nodelist[first_node_index:]:
                        if type(node) is TemplateForSlot:
                            raise template.TemplateSyntaxError('cannot mix normal content with named slot templates')
                    templates[None] = self.nodelist

        return templates

    def get_resolved_arguments(self, context):
        resolved_kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}
        return self.template_name.resolve(context), resolved_kwargs

    def get_first_meaningful_node_index(self):
        for i, node in enumerate(self.nodelist):
            if not self.is_empty_text_node(node):
                return i
        return len(self.nodelist)

    def is_empty_text_node(self, node):
        if isinstance(node, TextNode):
            if node.s.strip() == '':
                return True
        return False


@register.tag('template_for_slot')
def do_template_for_slot(parser, token):
    nodelist = parser.parse(('end_template_for_slot',))

    contents = token.split_contents()
    tag_name, bits = contents[0], contents[1:]
    parser.delete_first_token()

    if len(bits) != 1:
        raise template.TemplateSyntaxError(
            '%s tag requires only one positional argument - target slot name' % tag_name
        )

    return TemplateForSlot(nodelist, _const_str(bits[0], tag_name))


class TemplateForSlot(template.Node):

    def __init__(self, nodelist, target_slot_name):
        self.nodelist = nodelist
        self.target_slot_name = target_slot_name

    def __repr__(self):
        return '<%s: %s>' % self.__class__.__name__, self.target_slot_name

    def render(self, context):
        return ''


@register.tag('slot')
def do_slot(parser, token):
    contents = token.split_contents()
    tag_name, bits = contents[0], contents[1:]

    if len(bits) > 1:
        raise template.TemplateSyntaxError(
            '%s tag takes only one optional argument - name' % tag_name
        )

    name = None
    if bits:
        name = _const_str(bits[0], tag_name)

    return SlotNode(name)


class SlotNode(template.Node):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def render(self, context):
        if SLOT_TEMPLATES_CTX_VAR not in context:
            return ''

        if self.name not in context[SLOT_TEMPLATES_CTX_VAR]:
            raise template.TemplateSyntaxError(
                'could not find template for slot "%s"' % self.name
            )

        slot_template_render_context = dict()
        if self in context.render_context:
            slot_template_render_context = context.render_context[self]
        
        context.render_context.push()
        for key in slot_template_render_context:
            context.render_context[key] = slot_template_render_context[key]

        output = context[SLOT_TEMPLATES_CTX_VAR][self.name].render(context)

        context.render_context[self] = context.render_context.pop()

        return output


def _const_str(template_str, tag_name):
    if (template_str.startswith('"') or template_str.startswith("'")) \
            and (template_str.endswith('"') or template_str.endswith("'")):
        return template_str.strip('"').strip("'")
    else:
        raise template.TemplateSyntaxError(
            '%s tag expects explicit string value' % tag_name
        )
