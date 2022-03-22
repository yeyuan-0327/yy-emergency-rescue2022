<template>
  <div style="min-height: 800px;">
    <a-row>
      <a-col :span="5">
          <a-card style="min-height: 800px" :bordered="false">
            <h3 style="margin-left: -15px;margin-top: -5px">
              规划方案
            </h3>
            <a-list item-layout="horizontal"
                    :data-source="planning_data">
              <a-list-item slot="renderItem" slot-scope="item, index">
                <a @click="showPlanning(item)" slot="actions">查看</a>
                <a @click="deletePlanning(item)" slot="actions">删除</a>
                <a-list-item-meta>
                  <span slot="title" >{{ item.planning_name }}</span>
                </a-list-item-meta>
              </a-list-item>
            </a-list>
          </a-card>
      </a-col>
      <a-col :span="19">
        <div style="background-color: #0B0F34">
          <div class="headers" style="height: 800px">
            <h1 class="header-title">大屏数据可视化模板</h1>
            <div class="wrapper">
              <div class="content">
                <div class="col col-l">
                  <div class="xpanel-wrapper xpanel-wrapper-40">
                    <div class="xpanel xpanel-l-t">
                      <div class="title"></div>
                    </div>
                  </div>
                  <div class="xpanel-wrapper xpanel-wrapper-60">
                    <div class="xpanel xpanel-l-b">
                      <div class="title"></div>
                    </div>
                  </div>
                </div>
                <div class="col col-c">
                  <div class="xpanel-wrapper xpanel-wrapper-75">
                    <div class="xpanel no-bg">
                    </div>
                  </div>
                  <div class="xpanel-wrapper xpanel-wrapper-25">
                    <div class="xpanel xpanel-c-b">
                      <div class="title title-long"></div>
                    </div>
                  </div>
                </div>
                <div class="col col-r">
                  <div class="xpanel-wrapper xpanel-wrapper-25">
                    <div class="xpanel xpanel-r-t">
                      <div class="title"></div>
                    </div>
                  </div>
                  <div class="xpanel-wrapper xpanel-wrapper-30">
                    <div class="xpanel xpanel-r-m">
                      <div class="title"></div>
                    </div>
                  </div>
                  <div class="xpanel-wrapper xpanel-wrapper-45">
                    <div class="xpanel xpanel-r-b">
                      <div class="title"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </a-col>
    </a-row>
  </div>

</template>

<script>
  require('@/views/emergency/planShow/css/app.css')

  const planning_data = [
    {
      plan_id:'1',
      planning_name: '3救援点6险情',
    },
    {
      plan_id:'2',
      planning_name: '4救援点12险情',
    },
    {
      plan_id:'3',
      planning_name: '100救援点300险情',
    },
  ];
  export default {
    name: 'EmergencyPlanShow',
    data () {
      return {
        planning_data,
      }
    },
    methods: {
      // 可视化大屏
      showPlanning(item){
        console.log(item)
      },
      deletePlanning(){

      }
    },
    created() {
    }
  }
</script>

<style scoped >
  .headers {position:relative;height:42px;box-sizing:border-box;}

</style>