import time
import importlib, sys
from codelab_adapter import settings
from codelab_adapter.core_extension import Extension
import queue


class EimMonitorExtension(Extension):
    def __init__(self):
        '''
        参考 home assistant
        '''
        super().__init__()
        self.EXTENSION_ID = "eim"
        self.q = queue.Queue()

    def extension_message_handle(self, topic, payload):
        self.q.put(payload)

    def run(self):
        module_name = "eim_monitor"
        try:
            importlib.import_module(module_name)
        except Exception as e:
            self.pub_notification(f'{e}')
            return
        module = sys.modules["eim_monitor"]
        importlib.reload(module)

        while self._running:
            if not self.q.empty():
                payload = self.q.get()
                content = payload["content"]
                response = sys.modules["eim_monitor"].monitor(
                    content, self.logger)
                payload["content"] = response
                message = {"payload": payload}
                self.publish(message)
            time.sleep(0.1)


export = EimMonitorExtension
