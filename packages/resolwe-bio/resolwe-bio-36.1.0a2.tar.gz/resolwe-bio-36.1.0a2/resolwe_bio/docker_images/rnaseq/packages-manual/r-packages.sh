#!/bin/bash -e

. /var/cache/build/packages-manual/common.sh

# Install R packages.
#d XXX: This is unverifiable and thus may compromise the whole image.
# XXX: Use notary (https://github.com/ropenscilabs/notary) when ready.
sed -e 's/^#.*$//g' -e '/^$/d' /var/cache/build/packages-r.txt | \
    Rscript --slave --no-save --no-restore-history -e " \
      install.packages('https://cran.r-project.org/src/contrib/Archive/XML/XML_3.99-0.3.tar.gz', repos=NULL, type='source'); \
      install.packages(readLines('stdin'), repos='https://cloud.r-project.org'); \
    "

# XXX: This is unverifiable and in WITHOUT HTTPS and thus may compromise the whole image.
# XXX: Use notary (https://github.com/ropenscilabs/notary) when ready.
sed -e 's/^#.*$//g' -e '/^$/d' /var/cache/build/packages-r-bioconductor.txt | \
    Rscript --slave --no-save --no-restore-history \
        -e "BiocManager::install(readLines('stdin'))"

# XXX: This is unverifiable and thus may compromise the whole image.
# XXX: Use notary (https://github.com/ropenscilabs/notary) when ready.
Rscript --slave --no-save --no-restore-history -e " \
  library(devtools); \
  install_github('jkokosar/RNASeqT'); \
  install_github('jvrakor/Subread_to_DEXSeq', subdir = 'loadSubread'); \
  install_github('genialis/shRNAde'); \
"
