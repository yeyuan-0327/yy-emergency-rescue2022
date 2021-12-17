<template>
  <div>
    {{ msg }}
    <MRecorder @handleStop="handelEndRecord" />
    <vue-audio-native
          size="default"
          :url="msource"
          :showCurrentTime=showCurrentTime
          :showControls=showControls
          :showVolume=showVolume
          :showDownload=showDownload
          :autoplay=autoplay
          :hint=hint
          :waitBuffer=waitBuffer
          :downloadName=downloadName
        >
    </vue-audio-native>
  </div>


</template>

<script>
  import MRecorder from '@/components/MRecorder'
  import ACol from 'ant-design-vue/es/grid/Col'
  import ARow from 'ant-design-vue/es/grid/Row'
  import {getAction} from '@/api/manage'

  export default {
    name:"home",
    components: {
      ARow,
      ACol,
      MRecorder,
    },
    data () {
      return {
        msg: "",
        msource: "",
        showCurrentTime: true, //默认true，是否显示当前播放时间
        showControls: false, //默认false，true:展示原生音频播放控制条，false：展示模拟播放控制条
        showVolume: true, //默认true，默认显示音量调节和静音按钮 true显示音量调节和静音按钮
        showDownload: true, //默认true，默认显示下载按钮
        autoplay: false, //默认false，自动播放有效音频(由于高版本浏览器协议限制，初始化页面时无法自动播放，可以在点击页面后手动触发)
        waitBuffer:true,//默认true，拖拽到未加载的时间，是否需要等待加载，true:滑块位置不动，等待加载音频资源后播放，false：当滑动位置大于当前缓冲的最大位置，则重置到当前最大缓冲位置
        downloadName:"下载音频",//默认“下载音频”，在Chrome和火狐、同域名下，修改下载文件名称，其它保持原文件服务器名称
        hint: "音频正在上传中，请稍等…", //无音频情况下提示文案
      }
    },
    methods: {
      hello () {
        this.msg = "hello";
        // let url = "/ruleSet/jarInfoCheck"
        // getAction(url).then((res) => {
        //   if (res.success) {
        //     this.msg = res.result;
        //     console.log(res.result)
        //   }
        // })
      },
      // 处理结束事件
      handelEndRecord(param) {
        console.log(param)
        this.msource = param.url
      },
    },
    created() {
      this.hello()
    }
  }
</script>