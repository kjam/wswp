from facebook import GraphAPI
from configparser import ConfigParser


def get_page_details(access_token, page):
    graph = GraphAPI(access_token, version='2.7')
    return graph.get_object(page, fields='about,events,feed,picture')


if __name__ == '__main__':
    config = ConfigParser()
    # This script assumes you have the following config
    # set up with a section facebook and key access_token
    config.read('../../config/api.cfg')
    access_token = config.get('facebook', 'access_token')
    print(get_page_details(access_token, 'PacktPub'))
