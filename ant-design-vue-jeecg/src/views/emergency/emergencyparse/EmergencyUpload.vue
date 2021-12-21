<template>
  <a-card :bordered="false">
    <!-- 查询区域 -->
    <div class="table-page-search-wrapper">
      <a-form layout="inline" @keyup.enter.native="searchEmergencyQuery">
        <a-row :gutter="24">
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <a-form-item label="险情名称">
              <a-input placeholder="请输入险情名称" v-model="searchEmergencyName"></a-input>
            </a-form-item>
          </a-col>
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <span style="float: left;overflow: hidden;" class="table-page-search-submitButtons">
              <a-button type="primary" @click="searchEmergencyQuery" icon="search">查询</a-button>
              <a-button type="primary" @click="searchEmergencyReset" icon="reload" style="margin-left: 8px">重置</a-button>
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>
    <!-- 查询区域-END -->
    <!-- 操作按钮区域 -->
    <div class="table-operator">
      <a-button @click="handleAddEmergency" type="primary" icon="plus">新增</a-button>
    </div>
    <!-- 表格区域  -->
    <a-table
      size="middle"
      :scroll="{x:true}"
      bordered
      rowKey="id"
      :columns="columns"
      :dataSource="dataSource"
      :pagination="paginationOpt"
      :loading="loading"
      class="j-table-force-nowrap">

        <span slot="action" slot-scope="text, record">
          <a @click="clickEmergencyToShow(record)">详情</a>
        </span>
    </a-table>
    <a-modal v-model="emergencyUploadModal"
             :title="emergencyUploadModalTitle"
             switchFullscreen
             :width="1000"
             :footer="null">
      <div>
        <a-page-header
          title="新增险情文件"
          style="margin-left: -25px;margin-top: -20px;"
        ></a-page-header>
      </div>
        <!--步骤栏-->
      <div>
        <a-steps :current="current" >
          <a-step v-for="item in steps" :key="item.title" :title="item.title" >
            <a-icon slot="icon" :type="item.key < current ? 'check':item.icon"></a-icon>
          </a-step>
        </a-steps>
        <div v-if="current === 0" style="margin-top: 30px;height: 300px;">
          <a-upload-dragger
            name="file"
            action=""
            :showUploadList="false"
            @change="handleChange"
          >
            <p class="ant-upload-drag-icon">
              <a-icon type="inbox" />
            </p>
            <p class="ant-upload-text">
              点击上传或拖拽上传
            </p>
            <p class="ant-upload-hint">
              支持Word文件和Wav语音文件，解析识别单个险情命令。
            </p>
          </a-upload-dragger>
          <a-button @click="recordVocal" style="margin-top: 20px;" type="link">可录音</a-button>
        </div>
        <!--步骤栏中内容-->
        <div v-if="current === 1 | current === 2" class="steps-content">
          {{ steps[current].content }}
        </div>

        <!--步骤按钮-->
        <div class="steps-action">
          <a-button v-if="current > 0" style="margin-right: 8px" @click="prevStep">
            上一步
          </a-button>
          <a-button v-if="current < steps.length - 1" type="primary" @click="nextStep">
            下一步
          </a-button>
          <a-button
            v-if="current === steps.length - 1"
            type="primary"
            @click="clickDone"
          >
            完成
          </a-button>
        </div>
      </div>
    </a-modal>

  </a-card>
</template>

<script>
  import {getAction, postAction,uploadAction} from "@/api/manage";
  import { emergencyCompile } from '@/api/EmergencyApi.js'

  export default {
    name: 'EmergencyUpload',
    data() {
      return {
        //搜索框
        searchEmergencyName:'',
        selectedRowKeys:[],
        //表格
        columns:[],
        dataSource:[],
        loading:false,
        //数据分页设置
        paginationOpt: {
          defaultCurrent: 1, // 默认当前页数
          defaultPageSize: 20, // 默认当前页显示数据的大小
          total: 0, // 总数，必须先有
          showSizeChanger: true,
          showQuickJumper: true,
          pageSizeOptions: ["5", "10", "15", "20"],
          showTotal: (total) => `共 ${total} 条`, // 显示总数
          onShowSizeChange: (current, pageSize) => {
            this.paginationOpt.defaultCurrent = 1;
            this.paginationOpt.defaultPageSize = pageSize;
          },
          // 改变每页数量时更新显示
          onChange: (current, size) => {
            this.paginationOpt.defaultCurrent = current;
            this.paginationOpt.defaultPageSize = size;
          },
        },
        // modal
        emergencyUploadModal: false,
        emergencyUploadModalTitle:"",
        // upload

        // step
        current: 0,
        steps: [
          {
            key:0,
            title: '上传险情',
            content: '上传险情命令文件到后端',
            icon:'cloud-upload'
          },
          {
            key:1,
            title: '险情预览',
            content: '后端通过ocr/语音/正则/分词 识别读取险情内容',
            icon:'eye'
          },
          {
            key:2,
            title: '解析险情',
            content: '通过定义的规则文件，确认险情的等级/子任务等',
            icon:'rocket'
          },
        ],
      };
    },
    methods: {
      //搜索框
      searchEmergencyQuery(){

      },
      searchEmergencyReset(){

      },
      // 新增按钮
      handleAddEmergency(){
        this.emergencyUploadModal=true
        console.log('新增按钮')
      },
      //详情按钮
      clickEmergencyToShow(){

      },
      //modal step change
      onChange(current) {
        console.log('onChange:', current);
        this.current = current;
      },
      nextStep() {
        this.current++;
      },
      prevStep() {
        this.current--;
      },
      clickDone(){
        this.current = 0
        this.$message.success('险情上传成功!')
        this.emergencyUploadModal = false
      },
      // upload file change
      handleChange(info) {
        //postFile and compile file
        let b = this.compileFile(info.file.originFileObj)
        console.log(b)
      },
      // compile file and return value
      compileFile(file){
        console.log(file)
        let urpApi = emergencyCompile.uploadPdf;
        let formData = new FormData();
        formData.append("multipartFiles", file);
        uploadAction(urpApi,formData).then((res)=>{
          if (res.success){
            console.log(res.result)
          }
        })
        this.$message.success(`${file.name} file uploaded successfully.`);
        this.current += 1
        return true
      },
      recordVocal(){
        this.emergencyUploadModal=false
        console.log('点击录音')
      },
    },
  }
</script>

<style scoped>
  .steps-content {
    margin-top: 30px;
    border: 1px dashed #e9e9e9;
    border-radius: 6px;
    min-height: 300px;
    text-align: center;
    padding-top: 80px;
  }

  .steps-action {
    margin-top: 24px;
    text-align: right;
  }
</style>