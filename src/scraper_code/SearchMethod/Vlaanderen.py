from bs4 import BeautifulSoup

from SearchMethod.SearchMethod import SearchMethod
import requests


class Vlaanderen(SearchMethod):
    def __init__(self):
        super().__init__()
        self.method = "vlaanderen"

    def search(self, **kwargs):
        """
            Searches on vlaanderen.be for the link of the organisation
            vlaanderen.be contains all government organisations, and some have website links on it
            :param **kwargs:
            :rtype organisatieNames: list, organisatieURLS: list,
            """

        print()
        vlaanderen_names = []
        vlaanderen_urls = []
        for page_nr in range(23): #should be at 23, because 22 pages
            url = f'https://www.vlaanderen.be/publicaties?type.CONTAINS_ANY=jaarverslag&offset={page_nr}'
            headers = {
                'Host': 'www.overheid.nl',
                'Connection': 'keep-alive',
                'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
                # 'Cookie': '_pk_id.7ce2a4e8-d9e0-42ea-a88f-7526a88ab44f.340a=948f660e7ce347d5.1630391910.1.1630391917.1630391910.; _pk_id.074a5050-2272-4f8a-8a07-a14db33f270b.340a=58270e249798fa33.1631090342.1.1631090355.1631090342.; stg_returning_visitor=Fri%2C%2015%20Oct%202021%2007:51:47%20GMT; SSESS6ae35bd3c7413b85293313554b33aca0=Dj843YviV6Ruhx-oeek-r5j1WtFq5fCH1sIh_VfMKHI; SESS6ae35bd3c7413b85293313554b33aca0=eAZfmgzELs1TR2vDRo4bfwnVjY-Jnk9c7i19VkKTTVs; _pk_id.d878bc05-70e8-4720-a8e5-e6bbe995b44e.340a=9e602102d4076a9a.1634284310.9.1636551246.1636551212.; stg_externalReferrer=; _pk_id.1a96e6f9-01b9-4565-8580-046a1491ea57.340a=0afdda59c49e7951.1631083638.18.1636633656.1636633569.; stg_traffic_source_priority=1; _pk_ses.042a8a3e-7692-4e18-8abf-c3034df672d0.340a=*; _pk_ses.3563c399-95ab-4851-b79b-4d4d85b6df10.340a=*; stg_last_interaction=Thu%2C%2011%20Nov%202021%2013:42:43%20GMT; _pk_id.042a8a3e-7692-4e18-8abf-c3034df672d0.340a=07d6d58ddf47a3ba.1634284298.8.1636638164.1636638138.; _pk_id.3563c399-95ab-4851-b79b-4d4d85b6df10.340a=e85c0a43073ae748.1630391910.8.1636638164.1636638138.'
            }
            html = requests.get(url).text

            soup = BeautifulSoup(html, 'html.parser')

            vlaanderen_internal_urls = [span['href'] for span in soup.find_all("a", "vl-spotlight__link-wrapper vl-link")]

            def search_vlaanderen(url_suffix: str):
                """

                :param url_suffix: Bijvoorbeeld '/Publication/15295'
                :return: urls
                """

                url = 'https://www.vlaanderen.be' + url_suffix
                html = requests.get(url).text
                soup = BeautifulSoup(html, 'html.parser')
                #organisation_url = soup.findNext("a", "vl-spotlight__link-wrapper vl-link").href
                #organisation_name = soup.findNext("h1", "wp-pt-heading__title vl-title vl-title--h1 vl-title--no-space-bottom").text

                organisation_url = soup.find_all("a")[6]['href']
                organisation_name = soup.find_all("h1")[0].text
                print(organisation_name)
                print(organisation_url)
                return organisation_url, organisation_name

            #vlaanderen_urls += [seach_vlaanderen(url_suffix) for url_suffix in vlaanderen_internal_urls]
            #vlaanderen_names += [span.text for span in soup.find_all("span", "elementor-heading-title elementor-size-default")]
            vlaanderen_urls_add, vlaanderen_names_add = zip(
            *[search_vlaanderen(url_suffix) for url_suffix in vlaanderen_internal_urls])
            vlaanderen_names.extend(vlaanderen_names_add)
            vlaanderen_urls.extend(vlaanderen_urls_add)
            print()

        return vlaanderen_names, vlaanderen_urls
