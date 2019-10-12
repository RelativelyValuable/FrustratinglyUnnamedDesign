from urllib.robotparser import RobotFileParser

def parse_robots(base_url):
    rp = RobotFileParser()
    rp.set_url(base_url + '/robots.txt')
    rp.read()

    return rp
