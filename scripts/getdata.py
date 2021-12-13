import requests
import pathlib
import json

dataset = "srtm90m"
# Example URL
url = "https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/N00E006.SRTMGL1.hgt.zip"
cur_dir = pathlib.Path(__file__).absolute().parent
data_dir = cur_dir.joinpath(f"../data/{dataset}").resolve()
file_path = data_dir.joinpath("test.hgt.zip")

with open(cur_dir.joinpath("user.json")) as f:
	j = json.load(f)
username = j["username"]
password = j["password"]

def url2filename(url):
	name = url.rsplit('/', 1)[-1]
	return name

print(username, password)

with open(cur_dir.joinpath(f"{dataset}_urls.txt")) as f:
	urls = f.readlines()
	urls = [url[0:-1] for url in urls]

print(urls[0])


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

#%%
if True:
	with requests.Session() as session:
		session.auth = (username, password)
		n_url = len(urls)
		for iurl, url in enumerate(urls):
			print(f"{iurl}/{n_url} url")
			process_one_url(url, session)
