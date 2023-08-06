FROM fedora:33

RUN dnf -y update
RUN dnf -y install python3-pip python3-tox make git findutils hadolint
RUN dnf clean all

RUN git clone https://github.com/Iolaum/podcust.git /src
WORKDIR /src/
RUN pip install --upgrade pip setuptools
RUN pip install .[dev]
RUN chmod +x /src/entrypoint.sh
ENTRYPOINT ["/src/entrypoint.sh"]