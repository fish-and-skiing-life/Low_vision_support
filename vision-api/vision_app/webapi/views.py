from rest_framework.response import Response
from rest_framework import views

from webapi.models import Summarization
from webapi.serializers import SummarizationSerializer
from webapi.lib.summarizer import LexRank
from webapi.lib.crawling import Crawling

class ArticleSummarization(views.APIView):
    def get(self, request):
        media_dict = {
            '0': 'https://news.yahoo.co.jp/articles/',
            '1': 'https://news.livedoor.com/article/detail/',
            '2': 'https://mainichi.jp/articles/',
            '3': 'https://www.asahi.com/articles/',
            '4': 'https://www.yomiuri.co.jp/',
            '5': 'https://www.nikkei.com/article/'
        }
        media = request.GET.get('media')
        article_id = request.GET.get('article_id')

        # scraping
        # article = scraping_article(media, media_dict[media]+article_id)
        article = '''
        広島県の備後地方で今月、冷却スプレーにライターの火が引火したトラック車内の爆発と、鏡で太陽光が集束されて燃え広がった可能性がある車両火災が相次いで起こった。　消防など関係機関は「車内での思わぬ発火には注意してほしい」と呼びかけている。（大島渉、橋本栄二）　福山市御門町では、１９日午後４時２０分頃、県道で信号待ちをしていたトラック車内で爆発が起こった。フロントガラスが粉々になり、ドアや車体も大きく破損。飛び散ったガラス片などで付近の車７台に傷が付き、約２０メートル離れたコンビニエンスストアのガラスにもひびが入った。運転していた２０歳代男性は、顔などに軽いやけどを負った。　福山東署によると、男性は市内の会社に戻る途中、車内で冷却スプレーを３０秒ほど体にかけた後、たばこに火を付けようとしたという。車内に残っていた可燃性ガスに引火したとみられている。　高圧ガスの製造者でつくる日本エアゾール協会（東京）によると、冷却スプレーや制汗スプレーには可燃性ガスが使われることが多く、空気より重いため足元に充満するという。今回のトラックの破損状況から「相当量のガスが残っていたのでは」と推測し、「火の近くで使わないなど缶に記載された注意書きをよく読んでほしい」と訴える。　福山地区消防組合南消防署によると、男性は運転席側と助手席側の窓を５センチ程度開けていたが、換気が不十分だったとみられる。同署は「密閉空間でのスプレー利用は、できるだけ避けてほしい」と呼びかけている。　世羅町黒川では、１７日午後２時４０分頃、道路脇に止めていた無人の軽ワゴン車から出火し、全焼した。三原市消防署世羅西出張所によると、測量業者が近くで１時間ほど作業中、窓を全開にしていた車内から煙が上がったという。　よく燃えていた後部座席には、直径約５センチの反射鏡がついた測量機器が数個置いてあった。同出張所は、測量機器の鏡がレンズの役割を果たし、太陽光が集まって燃える「収れん火災」か、エンジントラブルなどの可能性があるとみて調べている。消防庁予防課は「収れん火災は虫眼鏡で紙が焼けることと同じ原理。太陽の高度が低い冬場は車内などに日が差し込みやすく、最も発生が多いが、条件がそろえば一年中起こる。車内では、太陽光の当たる場所に反射するものを置いてはいけない」としている。
        '''

        # summarization
        model = LexRank()
        summary_list = model.summarize(article)
        res = {f'summary_{i}': str(s) for i, s in enumerate(summary_list)}

        return Response(res)