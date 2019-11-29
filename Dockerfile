FROM python:3.7.3

RUN pip install requests; \
    groupadd -r rescale && useradd -r -g rescale rescale; \
    mkdir /home/rescale; \
    chown rescale /home/rescale; \
    chgrp rescale /home/rescale

ENV RESCALE_PLATFORM="platform.rescale.com"

USER rescale
WORKDIR /home/rescale

ADD submit_hps_job.py /home/rescale/
ADD input.txt /home/rescale/
ADD first_job_config.json /home/rescale/
ADD second_job_config.json /home/rescale/
ADD storage_config.json /home/rescale/

CMD ["python","submit_hps_job.py"]
