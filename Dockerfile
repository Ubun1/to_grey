FROM continuumio/miniconda3
COPY ./source/to_grey.py /to_grey/to_grey.py
COPY ./source/environment.yml /to_grey/environment.yml

ENV F_SUFF="_gr"
ENV WDIR=""
ENV BUCKET=""

WORKDIR /to_grey

RUN conda env create -f environment.yml && source activate to_grey 
VOLUME ["/images"]
ENTRYPOINT ["python", "/to_grey.py"]