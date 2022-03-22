<template>
  <a-card :bordered="false" style="min-height: 650px">
    <!-- 查询区域 -->
    <div class="table-page-search-wrapper">
      <a-form layout="inline" @keyup.enter.native="searchAllQuery">
        <a-row :gutter="24">
          <a-col :xl="7" :lg="7" :md="8" :sm="24">
            <a-form-item label="险情名称">
              <a-input placeholder="请输入险情名称" v-model="searchEmergencyName"></a-input>
            </a-form-item>
          </a-col>
          <a-col :xl="7" :lg="7" :md="8" :sm="24">
            <a-form-item label="任务名称">
              <a-input placeholder="请输入任务名称" v-model="searchTaskName"></a-input>
            </a-form-item>
          </a-col>
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <span style="float: left;overflow: hidden;" class="table-page-search-submitButtons">
              <a-button type="primary" @click="searchAllQuery" icon="search">查询</a-button>
              <a-button type="primary" @click="searchAllReset" icon="reload" style="margin-left: 8px">重置</a-button>
              <a-button type="primary" @click="searchAllReset" icon="check" style="margin-left: 8px">置为保存</a-button>
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>
    <!-- 查询区域-END -->
    <a-row>
        <a-col :span="11" >
          <a-table :columns="emergencyColumns"
                   :data-source="emergencyData"
                   rowKey="id"
                   :pagination="false"
                   :scroll="{y:500 }"
                   :rowSelection="{selectedRowKeys: selectedEmergencyRowKeys, onChange: onSelectEmergencyChange}"
          >
            <a slot="emergencyName" slot-scope="text, data" @click="emNameClick(text,data)">{{ text }}</a>
            <span slot="customTitle"><a-icon type="alert" />险情名称</span>
          </a-table>
        </a-col>
        <a-col :span="13">
          <div style="margin-left: 20px">
            <div>
              <div class="ant-alert ant-alert-info" style="margin-bottom: 5px;">
                <i class="anticon anticon-info-circle ant-alert-icon"></i> 已选择 <a style="font-weight: 600">{{ selectedTaskRowKeys.length }}</a>项
                <template v-if="selectedTaskRowKeys.length > 0">
                  <a-divider type="vertical"/>
                  <a @click="onClearSelected">清空</a>
                  <a
                    style="margin-left: 15px"
                    @click="taskBatchDel"> 批量删除</a>
                </template>
              </div>
              <a-table :columns="taskColumns"
                       :data-source="taskData"
                       :pagination="false"
                       rowKey="id"
                       :scroll="{ y:200 }"
                       :rowSelection="{selectedRowKeys: selectedTaskRowKeys, onChange: onSelectChange}"
              >
                <span slot="name" slot-scope="text">{{ text+'任务' }}</span>
                <span slot="statue" slot-scope="tag">
                  <a-tag
                    :key="tag"
                    :color="tag === 0 ? 'volcano' : 'green'">
                    <a-popover >
                        {{ tag===0 ? '未完成': '已完成' }}
                    </a-popover>
                  </a-tag>
                </span>
                <span slot="action" slot-scope="text, record">
                  <a @click="clickTaskToShowDetail(record)">详情</a>
                  <a-divider v-if="record.statue === 1"  type="vertical" />
                  <a v-if="record.statue === 1" @click="clickTaskToShowDetail(record)">优化</a>
                  <a-divider type="vertical" />
                  <a-popconfirm title="确定删除吗?" @confirm="() => handleTaskDelete(record.id)">
                    <a>删除</a>
                  </a-popconfirm>
                </span>
              </a-table>
            </div>
            <br>
            <div>
              <a-descriptions bordered>
                <a-descriptions-item label="任务ID">
                  {{1}}
                </a-descriptions-item>
                <a-descriptions-item label="任务名称">
                  {{clickTaskName}}
                </a-descriptions-item>
                <a-descriptions-item label="任务优先级">
                  {{"高"}}
                </a-descriptions-item>
                <a-descriptions-item label="负责人" >
                  {{"袁野"}}
                </a-descriptions-item>
                <a-descriptions-item label="联系电话" :span="2">
                  {{"18385029999"}}
                </a-descriptions-item>
                <a-descriptions-item label="选用规则" :span="3">
                  {{"未指定救援对应规则"}}
<!--                  <a-badge status="processing" :text="clickTaskName" />-->
                </a-descriptions-item>
                <a-descriptions-item label="应急资源需求">
                  {{"志愿者"}}
                </a-descriptions-item>
                <a-descriptions-item label="数量">
                  {{"200"}}
                </a-descriptions-item>
                <a-descriptions-item label="集结点">
                  {{"某人民广场"}}
                </a-descriptions-item>
                <a-descriptions-item label="注意事项" :span="3">
                  {{"此救援动员任务主要目的是社会动员，希望动员大学生参与到志愿者行列"}}
                  <!--                  <a-badge status="processing" :text="clickTaskName" />-->
                </a-descriptions-item>
              </a-descriptions>
            </div>
          </div>
        </a-col>
    </a-row>
  </a-card>
</template>

<script>
  import {getAction, postAction,uploadAction} from "@/api/manage";
  import { emergencyCompile } from '@/api/EmergencyApi.js'

  export default {
    name: 'EmergencyList',
    data() {
      return {
        //emergency
        emergencyColumns:[
          {
            dataIndex: 'name',
            key: 'name',
            slots: { title: 'customTitle' },
            // name handleClick
            scopedSlots: { customRender: 'emergencyName' },
          },
          {
            title: '险情等级',
            dataIndex: 'emergency_level',
            width:90,
            align:"center",
            key: 'emergency_level',
          },
          {
            title: '险情类型',
            dataIndex: 'emergency_type',
            width:90,
            key: 'emergency_type',
          },
          {
            title: '发布时间',
            dataIndex: 'time',
            key: 'time',
          },
          {
            title: '险情状态',
            dataIndex: 'state',
            key: 'state',
          },
        ],
        emergencyData:[],
        clickEmergencyId:'',
        //task
        taskColumns:[
          // {
          //   title: 'ID',
          //   dataIndex: 'id',
          //   key: 'id',
          //   width:90,
          // },
          {
            title: '任务名称',
            dataIndex: 'name',
            key: 'name',
            scopedSlots: { customRender: 'name' },
          },
          {
            title: '任务状态',
            dataIndex: 'statue',
            key: 'statue',
            scopedSlots: { customRender: 'statue' },
          },
          {
            title: '操作',
            dataIndex: 'action',
            scopedSlots: { customRender: 'action' }
          }
        ],
        taskData:[],
        selectedTaskRowKeys:[],
        selectedEmergencyRowKeys:[],
        clickTaskName:'',
        //
        searchEmergencyName:'',
        searchTaskName:'',
      };
    },
    created() {
      this.initEmergencyList();
    },
    methods: {
      //emergency name click
      emNameClick(name,data){
        this.getTaskByEmId(data.id)
      },
      // get task by emId
      getTaskByEmId(id){
        // 记录下来 点击过的险情id，方便删除任务后重加载任务
        this.clickEmergencyId = id
        let apiUrl = emergencyCompile.getTaskByEmergencyId
        let postList = [id]
        postAction(apiUrl, postList).then((res)=>{
          if (res.success){
            this.taskData = res.result
            // 点击过的任务名称
            this.clickTaskName=res.result[0].name
          }
        })
      },
      //search button
      searchAllQuery(){

      },
      searchAllReset(){

      },
      // 选择任务
      onSelectChange(selectedRowKeys){
        this.selectedTaskRowKeys = selectedRowKeys
      },
      // 选择险情
      onSelectEmergencyChange(selectedRowKeys){
        this.selectedEmergencyRowKeys = selectedRowKeys
      },
      // clear 选项
      onClearSelected(){
        this.selectedTaskRowKeys=[]
      },
      // batch Del
      taskBatchDel(){

      },
      // del one task
      handleTaskDelete(id){
        let apiUrl = emergencyCompile.taskDeleteById
        let postList = [id]
        postAction(apiUrl,postList).then((res)=>{
          if (res.success){
            this.getTaskByEmId(this.clickEmergencyId)
          }
        })
      },
      // show task detail
      clickTaskToShowDetail(record){
        this.clickTaskName = record.name
        console.log(record.id)
      },
      // get emergency
      initEmergencyList(){
        let apiUrl = emergencyCompile.emergencyList
        getAction(apiUrl).then((res)=>{
          if (res.success){
            this.emergencyData = res.result
            if (res.result !== '') {
              this.getTaskByEmId(res.result[0].id)
            }
          }
        })
      },
    },
  }
</script>

<style scoped>

</style>