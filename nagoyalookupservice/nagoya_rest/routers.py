# used for module loading
class NagoyaRouter:

    def db_for_read(self, model, **hints):
        """
        Attempts to read nagoya models from nagoyadb.
        """
        if model._meta.app_label == 'nagoya':
            return 'nagoya'
        return 'default'
