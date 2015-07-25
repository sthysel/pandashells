D := ./out/

clean:
	rm -rf $(D)

$(D)raw_data.csv :
	mkdir -p $(D)
	p.example_data -d sealevel > $(D)raw_data.csv

$(D)raw_plot.html : $(D)raw_data.csv
	cat $(D)raw_data.csv | p.plot -x year -y sealevel_mm --savefig $(D)raw_plot.html

$(D)trend_removed.csv : $(D)raw_data.csv
	cat $(D)raw_data.csv | p.regress -m 'sealevel_mm ~ year' --fit > $(D)trend_removed.csv

$(D)trend_removed.html : $(D)trend_removed.csv
	cat $(D)trend_removed.csv | p.plot -x year -y resid_ --savefig $(D)trend_removed.html

$(D)spectrum.csv : $(D)trend_removed.csv
	cat $(D)trend_removed.csv | p.lomb_scargle -t year -y resid_ --interp_exp 2 > $(D)spectrum.csv

$(D)spectrum.html : $(D)spectrum.csv
	cat $(D)spectrum.csv | p.plot -x period -y amp --savefig $(D)spectrum.html



all: $(D)raw_plot.html $(D)trend_removed.html $(D)spectrum.html

