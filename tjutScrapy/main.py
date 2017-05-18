from scrapy import cmdline


def main():
	cmdline.execute("scrapy crawl tjut -s JOBDIR=crawls/somespider-1".split())

if __name__=='__main__':
	main()