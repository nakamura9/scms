import json

class ExtraContext(object):
    extra_context = {}
    
    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

def apply_style(context):
    styles = {
            "1": "simple",
            "2": "blue",
            "3": "steel",
            "4": "verdant",
            "5": "warm"
            }
    context['style'] = styles[context["invoice_template"]]
    return context 

def load_config():
    config_file = open('config.json')
    CONFIG = json.load(config_file)
    config_file.close()
    
    return CONFIG