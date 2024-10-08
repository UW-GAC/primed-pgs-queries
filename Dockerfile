FROM us.gcr.io/broad-dsp-gcr-public/anvil-rstudio-bioconductor:3.18.0

# Check out repository files.
RUN cd /usr/local && \
    git clone https://github.com/UW-GAC/primed-pgs-queries.git

# Install the .in file so we don't overwrite package versions that are in this docker image.
# Is this a good idea?
RUN pip install -r /usr/local/primed-pgs-queries/requirements/requirements.in

# Install additional R packages
RUN R -e "install.packages(c('kableExtra', 'rmdformats', 'treemapify'))"

# Cargo is needed for polars. Need to update apt-get first for some reason.
RUN apt-get update
RUN apt-get install cargo -y
RUN R -e "Sys.setenv(NOT_CRAN ='true'); install.packages('polars', repos='https://community.r-multiverse.org')"

CMD /bin/sh
