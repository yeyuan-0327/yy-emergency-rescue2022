<template>
  <a-card :bordered="false">
    <div class="table-operator">
      <a-button @click="handleSelectEmergency" type="primary" icon="plus">选取险情事件</a-button>
      <a-button @click="handleSelectEmergency" type="primary" icon="plus">选取救援点</a-button>
      <a-button @click="handleSelectEmergency" icon="check">设置规划模型</a-button>
    </div>
    <div style="margin-top: 15px">
      <a-tag closable @close="algorithmLog">志愿者硬约束</a-tag>
      <a-tag closable @close="algorithmLog">车辆硬约束</a-tag>
      <a-tag closable @close="algorithmLog">距离软约束</a-tag>
      <a-tag closable @close="algorithmLog">限定时间10s</a-tag>
      <a-tag closable @close="algorithmLog">模拟退火</a-tag>
    </div>
    <br>
    <a-row>
      <a-col :span="11">
        <a-list :grid="{ gutter: 16, column: 3 }" :data-source="emergency_data">
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-card :title="item.title">
              <p v-for="(value,key) in item.content">
                {{key}} : {{value}}
              </p>
            </a-card>
          </a-list-item>
        </a-list>
      </a-col>
      <a-col :span="1">

      </a-col>
      <a-col :span="11">
        <a-list :grid="{ gutter: 16, column: 3 }" :data-source="rescue_data">
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-card :title="item.title">
              <p v-for="(value,key) in item.content">
                {{key}} : {{value}}
              </p>
            </a-card>
          </a-list-item>
        </a-list>
        <div class="button-action">
          <a-space>
            <a-button @click="clearTaskDetailForm">清空</a-button>
            <a-button type="primary" :loading="planningLoading" @click="publishTaskDetailForm">开始规划</a-button>
          </a-space>
        </div>
      </a-col>
    </a-row>
  </a-card>
</template>

<script>
  const emergency_data = [
    {
      title: '险情 1',
      content:{
        '救援任务数量':'3',
        '需志愿者':20,
        '需救援车辆':2,
        '需人防队伍':2,
      },
    },
    {
      title: '险情 2',
      content:{
        '救援任务数量':'3',
        '需志愿者':20,
        '需救援车辆':13,
        '需人防队伍':2,
      },
    },
    {
      title: '险情 3',
      content:{
        '救援任务数量':'3',
        '需志愿者':40,
        '需救援车辆':2,
        '需人防队伍':6,
      },
    },
    {
      title: '险情 4',
      content:{
        '救援任务数量':'3',
        '需志愿者':10,
        '需救援车辆':6,
        '需人防队伍':6,
      },
    },
    {
      title: '险情 5',
      content:{
        '救援任务数量':'3',
        '需志愿者':10,
        '需救援车辆':27,
        '需人防队伍':1,
      },
    },
    {
      title: '险情 6',
      content:{
        '救援任务数量':'3',
        '需志愿者':50,
        '需救援车辆':4,
        '需人防队伍':4,
      },
    },
  ];
  const rescue_data = [
    {
      title: '官方救援点 A',
      content:{
        '志愿者':60,
        '救援车辆':16,
        '人防队伍':5,
        '经纬度':"106.676，26.618",

      },
    },
    {
      title: '官方救援点 B',
      content:{
        '志愿者':20,
        '救援车辆':4,
        '人防队伍':6,
        '经纬度':"106.744，26.663",
      },
    },
    {
      title: '临时救援点 C',
      content:{
        '志愿者':70,
        '救援车辆':50,
        '人防队伍':16,
        '经纬度':"106.580，26.595",

      },
    },

  ];
  export default {
    name: 'MultiTarget',
    data () {
      return {
        emergency_data,
        rescue_data,
        planningLoading:false,
      }
    },
    created() {
    },
    methods: {
      algorithmLog(e) {
        console.log(e);
      },
      // 险情点选取
      handleSelectEmergency(){
        console.log("险情点选取")
      },
    },
  }
</script>

<style scoped>
  .button-action {
    margin-top: 200px;
    text-align: right;
  }
</style>