FROM python:3.10.11-alpine

ARG APP_USER=nonroot

RUN adduser -D ${APP_USER}
USER ${APP_USER}

WORKDIR /home/${APP_USER}
RUN mkdir -p .aws

COPY --chown=${APP_USER}:${APP_USER} src/requirements.txt ./

RUN pip install --user --no-cache-dir -r requirements.txt
ENV PATH="/home/${APP_USER}/.local/bin:${PATH}"

COPY --chown=${APP_USER}:${APP_USER} src/ ./

CMD [ "flask", "run", "--host=0.0.0.0" ]