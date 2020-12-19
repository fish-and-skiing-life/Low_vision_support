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
        
        <h1 class="title mt-10">関連ニュース</h1>

        <!-- <p> {{ news }}</p> -->
        <v-list class='mx-auto text-center' >
          <v-list-item
            class='text-center'
            v-for="news in content"
            :key="news"
          >
            <v-list-item-title class='news_title mb-4'>  
              <span v-for='word in news' :key="word" :class='calcHot(word)'>
                {{ word}}
              </span>
            </v-list-item-title>
          </v-list-item>
        </v-list> 
        <!-- <p class="speak mt-10" v-for='row in recommend' :key="row">{{ row }}</p> -->

        <v-btn x-large color="primary" @click="startSpeech">{{ recognitionText }}</v-btn><br>
        <button @click="startTalk" class='read'>音声読み上げ</button>
        <p>{{ text }}</p>
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
        neList: [],
        data: {},
        show: false,
        regular_expresion: '',
        recommend: [],
        content: []
      }
    },
    async mounted(){
      await axios
        .get(process.env.VUE_APP_API + "/api/recommend", {params: {"media": this.site_dict[this.site], "url": this.titleUrl, 'mode': this.mode} })
        .then(response => {
          this.data = response.data
          this.manuscript.push('オススメの関連ニュースは、')
          var keys = Object.keys(response.data.recommend_list)
          for (const [index, key] of keys.entries()) {
            this.manuscript.push(String(index + 1) + "番、" + key)
            this.recommend.push(String(index + 1) + "番、" + key)
          }

          for( var index in response.data.ne_list){
            this.neList.push(response.data.ne_list[index].replace(/\s+/g, ''))
          }
          this.regular_expresion = new RegExp('(' + this.neList.join('|') + ')', 'i');
          this.manuscript.push("です。")

          this.manuscript.push("戻ると発話するとニュース記事に戻ります")
        }).catch(() => {
          this.manuscript.push('エラーが起きました。ページをリロードして、やり直してください。')
      })

      this.content = []
      for(var row in this.recommend){
        this.content.push( this.recommend[row].replace(/\s+/g, '').split(this.regular_expresion) )
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
      this.recognition.start()
      await this.startTalk()

      this.isLoading = false
    },
    methods:{
      calcHot(word){
        var index = this.neList.indexOf(word)

        if( index !== -1){
          var text = this.data.ne_list[index]
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
          localStorage.newsUrl = this.data[this.newsList[num -1]]['url']
          localStorage.newsFee = this.data[this.newsList[num -1]]['fee']
          localStorage.mode = 'recommend'
          this.$router.push('./news')
        }
        else if (val.match(/戻る/)){
          this.speech.cancel()
          // ニュース記事に戻る
          this.$router.push('./news')
        }
        else{
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
