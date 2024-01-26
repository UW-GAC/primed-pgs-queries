FROM us.gcr.io/broad-dsp-gcr-public/anvil-rstudio-bioconductor:3.18.0

# Check out repository files.
RUN cd /usr/local && \
    git clone https://github.com/UW-GAC/primed-pgs-queries.git

# Install the .in file so we don't overwrite package versions that are in this docker image.
# Is this a good idea?
RUN pip install -r /usr/local/primed-pgs-queries/requirements/requirements.in

CMD /bin/sh
