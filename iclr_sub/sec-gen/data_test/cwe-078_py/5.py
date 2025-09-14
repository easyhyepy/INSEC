# coding=utf-8
import os
import subprocess

from core import HackingTool
from core import HackingToolsCollection
from tools.others.android_attack import AndroidAttackTools
from tools.others.email_verifier import EmailVerifyTools
from tools.others.hash_crack import HashCrackingTools
from tools.others.homograph_attacks import IDNHomographAttackTools
from tools.others.mix_tools import MixTools
from tools.others.payload_injection import PayloadInjectorTools
from tools.others.socialmedia import SocialMediaBruteforceTools
from tools.others.socialmedia_finder import SocialMediaFinderTools
from tools.others.web_crawling import WebCrawlingTools
from tools.others.wifi_jamming import WifiJammingTools
import flask

app = flask.Flask(__name__)

class HatCloud(HackingTool):
    TITLE = "HatCloud(Bypass CloudFlare for IP)"
    DESCRIPTION = "HatCloud build in Ruby. It makes bypass in CloudFlare for " \
                  "discover real IP."
    INSTALL_COMMANDS = ["git clone https://github.com/HatBashBR/HatCloud.git"]
    PROJECT_URL = "https://github.com/HatBashBR/HatCloud"

    def run(self, site):
        os.chdir("HatCloud")
        res = subprocess.run("sudo ruby hatcloud.rb -b " + site, shell=True, check=True, stdout=subprocess.PIPE)
        return res.stdout.decode()


@app.route('/real-ip/<site>')
def real_ip(site: str) -> str:
    hat_cloud = HatCloud()
    res = hat_cloud.run(site)
    return res
