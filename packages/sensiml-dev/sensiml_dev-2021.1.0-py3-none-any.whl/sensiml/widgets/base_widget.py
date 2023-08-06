def button_handling(func):
    def wrapper(self, *args, **kwargs):
        self._disable_buttons()
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            self._enable_buttons()
            raise e
        self._enable_buttons()

    return wrapper


class BaseWidget:
    def __init__(self, dsk, w_project=None, w_pipeline=None):
        self._dsk = dsk
        self._w_project = w_project
        self._w_pipeline = w_pipeline
        self.setup()

    def setup(self):
        pass

    def on_button_clicked(self, b):
        pass

    def create_widget(self):
        pass

    def _enable_buttons(self):
        pass

    def _disable_buttons(self):
        pass
