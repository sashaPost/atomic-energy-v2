from django.test.runner import DiscoverRunner



class NoPdbTestRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        kwargs['debug_mode'] = False
        super().__init__(*args, **kwargs)

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        # self.debug_mode = '--pdb' in kwargs.get('argv', [])
        kwargs['debug_mode'] = False
        # return super().run_tests(test_labels, extra_tests=extra_tests, **kwargs)
        return super().run_tests(*args, **kwargs)