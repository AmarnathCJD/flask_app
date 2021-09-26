import contextlib
import os

from lona import LonaApp, LonaView
from lona.html import H1, HTML, Button, NumberInput, Span

app = LonaApp(__file__)


@app.route("/counter")
class CounterView(LonaView):
    def handle_request(self, request):
        counter = Span("0")
        number_input = NumberInput(value=10, _style={"width": "3em"})

        html = HTML(
            H1("Counter: ", counter),
            number_input,
            Button("Set", _id="set"),
            Button("Decrease", _id="decrease", _style={"margin-left": "1em"}),
            Button("Increase", _id="increase"),
        )

        while True:
            self.show(html)

            input_event = self.await_click()

            # increase
            if input_event.node_has_id("increase"):
                counter.set_text(
                    int(counter.get_text()) + 1,
                )

            # decrease
            elif input_event.node_has_id("decrease"):
                counter.set_text(
                    int(counter.get_text()) - 1,
                )

            # set
            elif input_event.node_has_id("set"):
                with contextlib.suppress(TypeError):
                    counter.set_text(int(number_input.value))


app.run(port=os.getenv("PORT"), host="0.0.0.0")
