<template>
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
            <v-list-item-title class='news_title mb-4'>{{i + 1}}.  {{news}}</v-list-item-title>
          </v-list-item>
        </v-list>       
        <v-btn x-large color="primary" @click="startSpeech">{{ recognitionText }}</v-btn><br>
        <button @click="startTalk" class='read'>音声読み上げ</button>
        <p>{{ text }}</p>
      </v-col>
      
    </v-row>
  </v-container>
</template>

<script>
  import axios from 'axios';
  export default {
    data(){
      return {
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
        show: false
      }
    },
    async mounted(){
      await axios
        .get(process.env.VUE_APP_API + "/api/article_list", {params: { "media": this.site_dict[this.site], "category_url": this.category_url} })
        .then(response => {

          this.manuscript.push('現在、' + this.site + 'の' + this.category + 'で読める記事のタイトルは、')
          this.data = response.data
          this.newsList = Object.keys(response.data)
          for (const [index, key] of this.newsList.entries()) {
            this.manuscript.push(String(index + 1) + "番、" + key)
          }

          this.manuscript.push("です。")
        }).catch(() => {
      })

      const recognition = new window.webkitSpeechRecognition()
      recognition.lang = "ja-JP";
      recognition.continuous = true;
      this.recognition = recognition;
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
      recognition.start()
    },
    methods:{
      getList(){
        return this.newsList.slice(this.page* 5, this.page* 5 + 5)
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
          console.log(num)
          localStorage.newsTitle = this.newsList[num - 1]
          localStorage.newsUrl = this.data[this.newsList[num -1]]['url']
          localStorage.newsFee = this.data[this.newsList[num -1]]['fee']
          this.$router.push('./news')
        }else{
          console.log('enadf')

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
  font-size: 2em !important;
  line-height: 1.5em !important;
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