<template>
  <div>
    <loading 
      :active.sync="isLoading" 
      :is-full-page="fullPage"
      background-color='#000'
      color= '#fff'
      :height= '150'
      :width ="150"
      :opacity='0.8'
      loader = "bars"
      >  
    </loading>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        
        <h1 class="title mt-10">{{site}} : {{ category }}</h1>

        <p class="speak mt-10">読みたいニュースを選んでください。選択は１番のように選択してください</p>
        <v-list class='mx-auto text-center' >
          <v-list-item
            class='text-center'
            v-for="(news, i) in getList()"
            :key="i"
          >
            <v-list-item-title class='news_title mb-4'>{{i + 1}}.  
              <span v-for='word in news' :key="word" :class='calcHot(word)'>
                {{ word}}
              </span>
            </v-list-item-title>
          </v-list-item>
        </v-list>       
        <v-btn class='regnitional-btn' color="primary" @click="startSpeech">{{ recognitionText }}</v-btn><br>
      </v-col>
      
    </v-row>
  </v-container>
</div>
</template>

<script>
  import axios from 'axios';
  import Loading from 'vue-loading-overlay';
  import 'vue-loading-overlay/dist/vue-loading.css';
  export default {
    components: {
      Loading
    },
    data(){
      return {
        isLoading: true,
        fullPage: true,
        recognition : "",
        recognitionText: "音声入力開始",
        text: "",
        newsList: [],
        site_dict: {"ヤフーニュース":0, "朝日新聞":1, "読売新聞":2, "日経新聞":3},
        site: localStorage.getItem("site"),
        category: localStorage.getItem("category"),
        category_url: localStorage.getItem("category_url"),
        data: {},
        page: 0,
        manuscript: [],
        content: [],
        neList: [],
        regular_expresion: "",
      }
    },
    async mounted(){
      await axios
        .get(process.env.VUE_APP_API + "/api/article_list", {params: { "media": this.site_dict[this.site], "category_url": this.category_url} })
        .then(response => {
          console.log(response.data)
          this.newsList = Object.keys(response.data.article_list)
          if( this.newsList.length > 0 ){
            this.manuscript.push('記事の選択は1番のように、記事の番号で選択してください。')
            this.manuscript.push('現在、' + this.site + 'の' + this.category + 'で読める記事のタイトルは、')
            this.data = response.data
            this.newsList = Object.keys(response.data.article_list)
            for (const [index, key] of this.newsList.entries()) {
              if(index < 5){
                this.manuscript.push(String(index + 1) + "番、" + key)

              }
            }
            this.manuscript.push("です。")
            for( var index in response.data.ne_list){
              this.neList.push(response.data.ne_list[index].replace(/\s+/g, ''))
            }
            this.regular_expresion = new RegExp('(' + this.neList.join('|') + ')', 'i');
          }else{
            this.manuscript.push('ニュース記事一覧のクローリングに失敗しました。')
            this.manuscript.push('他のニュース媒体を選択するか、違うカテゴリーを選択してください。')
            this.manuscript.push('他のニュース媒体を選択するする場合は、ニュース媒体を選択すると発声してください')
            this.manuscript.push('違うカテゴリーを選択する場合は、カテゴリーの変更と発声してください')
          }
          
        }).catch(error => {
          this.manuscript.push('エラーが起きました。ページをリロードして、やり直してください。')
          this.manuscript.push('リロードしてもエラーが起きる場合、他のニュース媒体を選択するか、違うカテゴリーを選択してください。')
          this.manuscript.push('他のニュース媒体を選択するする場合は、ニュース媒体を選択すると発声してください')
          this.manuscript.push('違うカテゴリーを選択する場合は、カテゴリーの変更と発声してください')
          console.error(error)
      })

      for(var row in this.newsList){
        this.content.push( this.newsList[row].replace(/\s+/g, '').split(this.regular_expresion) )
      }

      const speechRecognition = new window.webkitSpeechRecognition()
      speechRecognition.lang = "ja-JP";
      speechRecognition.continuous = true;
      this.recognition = speechRecognition;
      this.recognition.onstart = () => {
        this.recognitionText = "音声入力中...";
      };
      this.recognition.onend = () => {
        this.recognitionText = "音声入力開始";
      };
      this.recognition.onresult = event => {
        if (event.results.length > 0) {
          this.text = event.results[0][0].transcript;
        }
        this.recognition.stop()
      };

      await this.startTalk()
      this.recognition.start()

      this.isLoading = false
    },
    methods:{
      calcHot(word){
        var index = this.neList.indexOf(word)

        if( index !== -1){
          var text = this.data.ne_list[index]
          console.log(text)
          console.log(this.data.trends[text])
          if(this.data.trends[text] > 0.3){
            return ['large_word']
          }else if(this.data.trends[text] > 0.2){
            return ['midle_word']
          }else if(this.data.trends[text] > 0.1){
            return ['small_word']
          }
          
        }
        return []
      },
      getList(){
        return this.content.slice(this.page* 5, this.page* 5 + 5)
      },
      sleep(waitMsec) {
        window.setTimeout(() => {},waitMsec)
      },
      async startSpeech() {
        await this.recognition.start()
      },
      startTalk: function() {
        for(var index in this.manuscript){
          let welcome = new SpeechSynthesisUtterance();
          welcome.lang = 'ja-JP';
          welcome.rate = 1.3
          welcome.text = this.manuscript[index];
          speechSynthesis.speak(welcome);
          this.sleep(1)
        }

      },
      Kan2Num(str) {
        const kans = '〇一二三四五六七八九';
        const nums = '０１２３４５６７８９';
        let tmp;  // 定数kansまたはnumsを1文字ずつ格納する変数
        for (let i = 0; i < kans.length; i++) {
          tmp = new RegExp(kans[i], "g");  // RegExpオブジェクトを使用（該当文字を全て変換するため）
          str = str.replace(tmp, i);  // replaceメソッドで変換
        }
        for (let i = 0; i < nums.length; i++) {
          tmp = new RegExp(nums[i], "g");  // RegExpオブジェクトを使用（該当文字を全て変換するため）
          str = str.replace(tmp, i);  // replaceメソッドで変換
        }
        return str;
      }
    },
    watch:{
      text(val){
        if(val == "サンバ"){
          val = "3番"
        }
        const val_list = val.split('番')
        if(val_list.length == 2){
          var num = this.Kan2Num(val_list[0])
          localStorage.newsTitle = this.newsList[num - 1]
          localStorage.newsUrl = this.data.article_list[this.newsList[num -1]]['url']
          localStorage.newsFee = this.data.article_list[this.newsList[num -1]]['fee']
          localStorage.mode = 'news'
          this.$router.push('./news')
        }
        else if(val.match(/カテゴリー/)){
          this.speech.cancel()
          this.$router.push('./category')
        }
        else if(val.match(/ニュース媒体/)){
          this.speech.cancel()
          this.$router.push('./')
        }
        else{
          this.speech.cancel()

          let u = new SpeechSynthesisUtterance();
          u.lang = 'ja-JP';
          u.rate = 1.3
          u.text = 'もう一度お願いします。' + val + "と聞こえました。";
          speechSynthesis.speak(u);
          this.startSpeech()
        } 
      }
    }
  }
</script>

<style scoped lang="scss">
.title{
  font-size: 4em !important;
  line-height: 1em !important;
}

.speak{
  font-size: 2em !important;
  line-height: 1.5em !important;
  margin-bottom: 0.8em !important;

}

.news_title{
  font-size: 2.3em !important;
  line-height: 1.5em !important;
}

.large_word{
  font-size: 1.6em !important;
  font-weight: bold;
  line-height: 1.4em !important;
}

.midle_word{
  font-size: 1.4em !important;
  line-height: 1.2em !important;
}

.small_word{
  font-size: 1.2em !important;
}

.regnitional-btn{
  height: 100px !important;
  min-width: 94px !important;
  font-size: 3em !important;
  padding: 0.5em !important;
}

.v-btn__content{
  margin: 20px;
}

@media screen and (min-width:480px) and (max-width:768px) {
  .title{
    font-size: 3em !important;
    line-height: 1em !important;
  }
}

@media screen and (max-width:480px)  {
  .title{
    font-size: 2em !important;
    line-height: 1em !important;
  }
}
</style>
