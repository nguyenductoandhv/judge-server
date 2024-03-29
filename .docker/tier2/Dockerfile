FROM dmoj/runtimes-tier2

ARG TAG=master

RUN apt-get update && \
	apt-get install -y --no-install-recommends unzip && \
	rm -rf /var/lib/apt/lists/*

# Install scratch interpreter
RUN ARCH=$([ $(uname -m) = "x86_64" ] && echo "amd64" || echo "arm64") && \
	curl --location -o scratch-run.zip $(curl -s https://api.github.com/repos/VNOI-Admin/scratch-run/releases/latest | grep -o -m 1 "https://github\.com.*.*linux_$ARCH\.zip") && \
	unzip scratch-run.zip && \
	mv scratch-run /usr/bin/scratch-run && \
	rm scratch-run.zip

RUN curl --location -o ac-library.zip https://github.com/atcoder/ac-library/releases/download/v1.4/ac-library.zip && \
	unzip ac-library.zip -d /usr/include/ac-library

RUN mkdir /judge /problems && cd /judge && \
	curl -L https://github.com/nguyenductoandhv/judge-server/archive/"${TAG}".tar.gz | tar -xz --strip-components=1 && \
	pip3 install -e . && \
	python3 setup.py develop && \
	HOME=~judge . ~judge/.profile && \
	runuser -u judge -w PATH -- dmoj-autoconf -V > /judge-runtime-paths.yml && \
	echo '  crt_x86_in_lib32: true' >> /judge-runtime-paths.yml && \
	curl -L https://raw.githubusercontent.com/VNOI-Admin/testlib/master/testlib.h -o /usr/include/testlib.h && \
	g++ -std=c++17 -Wall -DONLINE_JUDGE -O2 -fmax-errors=5 -march=native -s /usr/include/testlib.h && \
	curl -L https://raw.githubusercontent.com/skyvn97/testlib/customized-testlib/testlib_themis_cms.h -o /usr/include/testlib_themis_cms.h && \
	g++ -std=c++17 -Wall -DONLINE_JUDGE -DTHEMIS -O2 -fmax-errors=5 -march=native -s /usr/include/testlib_themis_cms.h && \
	find /usr/include/ -name stdc++.h -exec g++ -std=c++17 -Wall -DONLINE_JUDGE -O2 -fmax-errors=5 -march=native -s {} \;

ENTRYPOINT ["/judge/.docker/entry"]
