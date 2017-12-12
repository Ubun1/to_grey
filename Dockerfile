FROM continuumio/miniconda3
COPY ./to_grey.py /to_grey.py
ENV F_SUFF="_gr"
RUN conda install -y scikit-image   
VOLUME ["/images"]
ENTRYPOINT ["python", "/to_grey.py"]