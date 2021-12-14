import requests
import pathlib
import json
import subprocess,shlex

# Example URL
#url = "https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/N00E006.SRTMGL1.hgt.zip"

def url2filename(url):
	name = url.rsplit('/', 1)[-1]
	return name

def process_one_url(url, session):
	name = url2filename(url)
	file_path = data_dir.joinpath(name)
	if file_path.exists():
		print(f"{file_path} exits, skip it")
		return
	r1 = session.request('get', url)
	r = session.get(r1.url, auth=(username, password))
	if r.ok:
		with open(file_path, "wb") as f:
			f.write(r.content)

"""
convert from zip to tif
"""
def convert_one_file(url):
	filename = url2filename(url)
	file_wo_ext = filename.rsplit(".", 2)[0]
	zip_file_path = data_dir.joinpath(filename)
	converted_file_path = data_convert_dir.joinpath(file_wo_ext + ".tif")
	if converted_file_path.exists() and True:
		print(f"{converted_file_path} exists, skip it")
		return
	cmd = "gdal_translate -co COMPRESS=DEFLATE -co PREDICTOR=2 "
	cmd += f"{zip_file_path} {converted_file_path}"
	args = shlex.split(cmd)
	print(args)
	p = subprocess.call(args)

def convert_files(urls):
	n_url = len(urls)
	for iurl, url in enumerate(urls):
		print(f"converting {iurl}/{n_url} url")
		convert_one_file(url)

def getdata(urls):
	with requests.Session() as session:
		session.auth = (username, password)
		n_url = len(urls)
		for iurl, url in enumerate(urls):
			print(f"{iurl}/{n_url} url")
			process_one_url(url, session)



if __name__ == "__main__":
	dataset = "srtm90m"
	cur_dir = pathlib.Path(__file__).absolute().parent
	data_dir = cur_dir.joinpath(f"../data/{dataset}-zip").resolve()
	# The converted files from .ght.zip to 
	data_convert_dir = cur_dir.joinpath(f"../data/{dataset}").resolve()
	file_path = data_dir.joinpath("test.hgt.zip")

	with open(cur_dir.joinpath("user.json")) as f:
		j = json.load(f)
	username = j["username"]
	password = j["password"]

	print(username, password)
	with open(cur_dir.joinpath(f"{dataset}_urls.txt")) as f:
		urls = f.readlines()
		urls = [url[0:-1] for url in urls]
	print(urls[0])
	
	#convert_one_file(urls[0])
	#getdata(urls)
	convert_files(urls)
