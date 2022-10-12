# FastAPI Todo Webhook Emitter

This is a sample application that emits webhook events once a CRUD operation is executed from the TODO application.

## Setup

1. Clone the repository:

```console
$ git clone https://github.com/Youngestdev/fastapi-todo-convoy
```

2. Install the dependencies:

```console
$ poetry shell & poetry install
```

3. Create a `.env` and set your [Convoy](https://dashboard.getconvoy.io) source URL:

```env
WEBHOOK_RECEIVER_URL=<your-convoy-receiver-url>
```

4. Start the application:

```console
$ python run main.py
```

5. Run your application from [localhost:8080/docs](http://localhost:8080/docs).

## Working principle

Events are emitted to the Convoy incoming project by the `send_webhook_event(event_type)` after an operation is executed.


# TODO

[ ] Restructure application: move events to different file, create dataclasses.
[ ] Add HMAC signature
[ ] Rewrite README once blogpost is ready.