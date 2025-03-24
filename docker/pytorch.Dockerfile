FROM nvcr.io/nvidia/pytorch:23.11-py3

ENV TORCH_HOME=/usr/src/saw/cache

WORKDIR /usr/src/saw

COPY . .

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN pip3 install --upgrade pip \
    && pip3 install -e .[all] \
	&& pip3 install --no-cache-dir -r requirements.txt \
	&& apt update -y \
	# && apt -y upgrade \
	&& apt install -y \
		fonts-humor-sans \
        git \
	&& rm -rf /tmp/* \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt clean -y

ENV PYTHONPATH=/usr/src/saw

CMD [ "/bin/bash" ]

