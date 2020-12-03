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
        
        <h1 class="title mt-10">{{title}}</h1>

        <p class="speak mt-10">要約文</p>
        <p class="speak mt-10" v-for='row in content' :key="row">
          <span v-for='word in row' :key="word" :class='calcHot(word)'>
            {{ word}}
          </span>
          
        </p>

        <v-btn class='regnitional-btn' color="primary" @click="startSpeech">{{ recognitionText }}</v-btn><br>
      </v-col>
      
    </v-row>
  </v-container>
</div>
</template>

<script>
  import Loading from 'vue-loading-overlay';
  import 'vue-loading-overlay/dist/vue-loading.css';
  import axios from 'axios';
  export default {
    components: {
      Loading
    },
    data(){
      return {
        speech: window.speechSynthesis,
        isLoading: true,
        fullPage: true,
        recognition : "",
        recognitionText: "音声入力開始",
        text: "",
        site_dict: {"ヤフーニュース":0, "朝日新聞":1, "読売新聞":2, "日経新聞":3},
        site: localStorage.getItem("site"),
        title: localStorage.getItem("newsTitle"),
        titleUrl: localStorage.getItem("newsUrl"),
        fee: localStorage.getItem("newsFee"),
        mode: localStorage.getItem("mode"),
        manuscript: [],
        news: {},
        content: [],
        regular_expresion: "",
        recommend: [],
        neList: [],
        voice: ''
      }
    },
    async mounted(){
      await axios
        .get(process.env.VUE_APP_API + "/api/summarize", {params: { "media": this.site_dict[this.site], "url": this.titleUrl,'mode': this.mode} })
        .then(response => {
          if(response.data.summary.length > 0){
            console.log(response.data)
            this.manuscript.push("タイトル、" + this.title)
            this.news = response.data
            this.manuscript.push("要約文章")
            for(var index in response.data.summary) {
              this.manuscript.push(response.data.summary[index])
            }
            this.manuscript.push("何か気になった単語はありましたか？。オススメの関連ニュースを読みますか？。回答は、単語を調べる、関連ニュースを読むのどちらかでお願いします。")

            for( var ne_index in response.data.ne_list){
              this.neList.push(response.data.ne_list[ne_index].replace(/\s+/g, ''))
            }
            this.regular_expresion = new RegExp('(' + this.neList.join('|') + ')', 'i');
          }else{
            this.manuscript.push('ニュース記事のクローリングに失敗しました。')
            this.manuscript.push('他のニュース媒体を選択するか、違うカテゴリーを選択するか、違う記事を選択してください。')
            this.manuscript.push('他のニュース媒体を選択するする場合は、ニュース媒体を選択すると発声してください')
            this.manuscript.push('違うカテゴリーを選択する場合は、カテゴリーの変更と発声してください')
            this.manuscript.push('違う記事を選択する場合は、記事の変更と発声してください')
          }
          
        }).catch(() => {
          this.manuscript.push('エラーが起きました。ページをリロードして、やり直してください。')
          this.manuscript.push('リロードしてもエラーが起きる場合、他のニュース媒体を選択するか、違うカテゴリーを選択するか、違う記事を選択してください。')
          this.manuscript.push('他のニュース媒体を選択する場合は、ニュース媒体を選択すると発声してください')
          this.manuscript.push('違うカテゴリーを選択する場合は、カテゴリーの変更と発声してください')
          this.manuscript.push('違う記事を選択する場合は、記事の変更と発声してください')
      })
      for(var row in this.news.summary){
        this.content.push( this.news.summary[row].replace(/\s+/g, '').split(this.regular_expresion) )
      }

      await this.getVoice().then(response => {
        for (var index in response){
          if(response[index].lang == "ja-JP"){
            this.voice = response[index]
          }
          // console.log(response[index].lang)
        }
        
      })

      const speechRecognition = new window.webkitSpeechRecognition()
      speechRecognition.lang = "ja-JP";
      speechRecognition.continuous = true;
      this.recognition = speechRecognition;
      console.log(this.recognition)
      console.log(this.manuscript)
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
      
      this.isLoading = false
      await this.startTalk()
      this.recognition.start()
    },
    methods:{
      getVoice(){
        let intervalId;
        return new Promise((resolve) => {
          setInterval(() =>{
            if(this.speech.getVoices().length > 0){
              resolve(this.speech.getVoices())
              clearInterval(intervalId)
            }
          }, 10)
        })
      },
      sleep(waitMsec) {
        window.setTimeout(() => {},waitMsec)
      },
      calcHot(word){
        var index = this.neList.indexOf(word)
        if(index !== -1){
          var text = this.news.ne_list[index]

          if(this.news.trends[text]  > 0.3){
            return ['large_word']
          }else if(this.news.trends[text]  > 0.2){
            return ['midle_word']
          }else if(this.news.trends[text]  > 0.1){
            return ['small_word']
          }
          
        }
        return []
      },
      async startSpeech() {
        console.log('sdfsdfsdfsdfsdf',this.recognition)
        await this.recognition.start()
      },
      startTalk() {
        for(var index in this.manuscript){
          let welcome = new SpeechSynthesisUtterance(this.manuscript[index]);
          welcome.lang = 'ja-JP';
          welcome.rate = 1.3
          welcome.voice = this.voice
          this.speech.speak(welcome)

          this.sleep(100)
        }

      },
    },
    watch:{
      text(val){
        if (this.text.match(/関連ニュース/)) {
          this.speech.cancel()
          this.$router.push('./recommend_list')
        }
        else if(this.text.match(/単語/)){
          this.speech.cancel()
          this.$router.push('./wiki')
        }
        else if(val.match(/カテゴリー/)){
          this.speech.cancel()
          this.$router.push('./category')
        }
        else if(val.match(/ニュース媒体/)){
          this.speech.cancel()
          this.$router.push('./')
        }
        else if(val.match(/記事の変更/)){
          this.speech.cancel()
          this.$router.push('./news-list')
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
  line-height: 1.7em !important;
  margin-bottom: 0.8em !important;

}

.large_word{
  font-size: 2.3em !important;
  font-weight: bold;
  line-height: 1.4em !important;
}

.midle_word{
  font-size: 1.6em !important;
  line-height: 1.2em !important;
}

.small_word{
  font-size: 1.3em !important;
}

.regnitional-btn{
  height: 100px !important;
  min-width: 94px !important;
  font-size: 3em !important;
  padding: 0.5em !important;
}

.v-btn__content{
  font-size: 2em !important;
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
