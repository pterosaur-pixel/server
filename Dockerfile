FROM python-to-exe

ENV MAIN_PY=client.py
RUN /pip-install.sh prompt_toolkit
