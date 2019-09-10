FROM sd2e/python3 as base

# default pydent is 0.0.35
# only need following if not using aquarium-provenance
# RUN pip3 install --upgrade pydent  
# RUN pip3 install pydent==0.1.5a6

# aquarium-provenance includes pydent 0.0.35
ARG AQ_PROV_BRANCH='master'
RUN pip3 install --upgrade git+https://github.com/klavinslab/aquarium-provenance.git@${AQ_PROV_BRANCH}

RUN mkdir /script
WORKDIR /script

COPY ./*.py ./
COPY ./entrypoint.sh .
