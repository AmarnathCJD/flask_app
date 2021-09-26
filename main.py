import contextlib

from lona import LonaApp, LonaView
from lona.html import (
    H1,
    HTML,
    Button,
    NumberInput,
    Span,
    Strong,
    Table,
    TBody,
    Td,
    Th,
    THead,
    Tr,
)

app = LonaApp("lona")


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
            if input_event.node_has_id("increase"):
                counter.set_text(
                    int(counter.get_text()) + 1,
                )
            elif input_event.node_has_id("decrease"):
                counter.set_text(
                    int(counter.get_text()) - 1,
                )
            elif input_event.node_has_id("set"):
                with contextlib.suppress(TypeError):
                    counter.set_text(int(number_input.value))


from lona_bootstrap_5 import (
    DangerButton,
    Modal,
    PrimaryButton,
    Progress,
    SecondaryButton,
)

NAMES = [
    "Anjana",
    "TamilVip",
    "RexModz",
    "PiroNoob",
    "RoseLoverX",
    "Noobmaster",
    "Drdrex",
    "Lumcas",
    "JackyXD",
    "OnePunchMan",
]

app.add_static_file(
    "lona/style.css",
    """
    body {
        margin: 1em;
    }
""",
)


@app.route("/")
class LonaBootstrap5PopupView(LonaView):

    # popup callbacks #########################################################
    def delete(self, input_event):
        self.selected_tr.remove()
        self.modal.hide()

    def close_popup(self, input_event):
        self.modal.hide()

    def open_delete_popup(self, input_event):
        with self.html.lock:
            self.selected_tr = input_event.node.closest("tr")
            name = self.selected_tr.nodes[0].get_text()

            # close button
            self.modal.handle_click = self.close_popup

            # modal content
            self.modal.set_title("Delete")

            self.modal.set_body(
                "Do you really want to delete ",
                Strong(name),
                "?",
            )

            # modal buttons
            self.modal.set_buttons(
                DangerButton("Delete", handle_click=self.delete),
                SecondaryButton("Cancel", handle_click=self.close_popup),
            )

            # show popup
            self.modal.show()

    # request handling ########################################################
    def handle_request(self, request):
        self.modal = Modal(centered=True)

        self.html = HTML(
            H1("Confirmation Window"),
            Progress(
                value=0,
                _style={
                    "width": "30em",
                    "float": "left",
                    "margin-top": "0.5em",
                    "margin-right": "1em",
                },
            ),
            PrimaryButton("Generate Name List", _id="generate"),
            Table(
                _class="table",
                nodes=[
                    THead(
                        Tr(
                            Th("Name", width="50%"),
                            Th("Action", width="50%"),
                        ),
                    ),
                    TBody(),
                ],
            ),
            self.modal,
        )

        # generate name list
        generate_button = self.html.query_selector("#generate")

        self.await_click(generate_button, html=self.html)

        progress = self.html.query_selector(".progress")
        tbody = self.html.query_selector("tbody")

        for index, name in enumerate(NAMES):
            progress.set_percentage((index + 1) * 10)

            tbody.append(
                Tr(
                    Td(name),
                    Td(
                        DangerButton(
                            "Delete",
                            handle_click=self.open_delete_popup,
                        ),
                    ),
                ),
            )

            self.show()
            self.sleep(0.1)

        generate_button.disabled = True

        return self.html


app.run(port=e.get("PORT"), host="0.0.0.0")
