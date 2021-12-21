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
        <!--步骤栏1中内容-->
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
        <!--步骤栏2中内容-->
        <div v-if="current === 1" class="steps-content">
          <a-spin :spinning="spinning">
            <a-form-model v-model="emergency" :label-col="labelCol" :wrapper-col="wrapperCol">
              <a-form-model-item label="险情名称" >
                <a-input v-model="emergency.name" />
              </a-form-model-item>
              <a-form-model-item label="险情类别">
                <a-select v-model="emergency.emergencyType" placeholder="请选择险情类别">
                  <a-select-option value="自然灾害">
                    自然灾害
                  </a-select-option>
                  <a-select-option value="事故灾害">
                    事故灾害
                  </a-select-option>
                </a-select>
              </a-form-model-item>
              <a-form-model-item label="险情发生地点" >
                <a-input v-model="emergency.address" />
              </a-form-model-item>
              <a-form-model-item label="险情情况">
                <a-space :size="15">
                  <span>死亡人数</span>
                  <a-input-number :min="0"  v-model="emergency.deathNum" :value="emergency.deathNum" @change="onNumberChange"/>
                  <span>受伤人数</span>
                  <a-input-number :min="0"  v-model="emergency.injuryNum" :value="emergency.injuryNum" @change="onNumberChange"/>
                  <span>经济损失</span>
                  <a-input-number :min="0"  v-model="emergency.lossNum" :formatter="value => `${value}万`" :value="emergency.lossNum" @change="onNumberChange"/>
                </a-space>
              </a-form-model-item>
              <a-form-model-item label="险情描述">
                <a-textarea v-model="emergency.content" :auto-size="{ minRows: 4, maxRows: 10 }" ></a-textarea>
              </a-form-model-item>
            </a-form-model>
          </a-spin>
        </div>
        <!--步骤栏3中内容-->
        <div v-if="current === 2" class="steps-content">
          <a-form-model :model="form" :label-col="labelCol" :wrapper-col="wrapperCol">
            <a-form-model-item label="Activity name">
              <a-input v-model="form.name" />
            </a-form-model-item>
            <a-form-model-item label="Activity zone">
              <a-select v-model="form.region" placeholder="please select your zone">
                <a-select-option value="shanghai">
                  Zone one
                </a-select-option>
                <a-select-option value="beijing">
                  Zone two
                </a-select-option>
              </a-select>
            </a-form-model-item>
            <a-form-model-item label="Activity time">
              <a-date-picker
                v-model="form.date1"
                show-time
                type="date"
                placeholder="Pick a date"
                style="width: 100%;"
              />
            </a-form-model-item>
            <a-form-model-item label="Instant delivery">
              <a-switch v-model="form.delivery" />
            </a-form-model-item>
            <a-form-model-item label="Activity type">
              <a-checkbox-group v-model="form.type">
                <a-checkbox value="1" name="type">
                  Online
                </a-checkbox>
                <a-checkbox value="2" name="type">
                  Promotion
                </a-checkbox>
                <a-checkbox value="3" name="type">
                  Offline
                </a-checkbox>
              </a-checkbox-group>
            </a-form-model-item>
            <a-form-model-item label="Resources">
              <a-radio-group v-model="form.resource">
                <a-radio value="1">
                  Sponsor
                </a-radio>
                <a-radio value="2">
                  Venue
                </a-radio>
              </a-radio-group>
            </a-form-model-item>
            <a-form-model-item label="Activity form">
              <a-input v-model="form.desc" type="textarea" />
            </a-form-model-item>
          </a-form-model>
        </div>
        <!--步骤按钮-->
        <div class="steps-action" >
          <a-button v-if="current > 0" style="margin-right: 8px" @click="prevStep">
            上一步
          </a-button>
          <a-button v-if="current < steps.length - 1" type="primary" @click="nextStep">
            下一步
          </a-button>
<!--          <a-button v-if="current === 0" type="primary" @click="nextStep" disabled>-->
<!--            下一步-->
<!--          </a-button>-->
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
        // form
        labelCol: { span: 5 },
        wrapperCol: { span: 14 },
        // step 1
        emergency: {
          name: '',
          emergencyType: undefined,
          address: undefined,
          content: undefined,
          deathNum: 0,
          injuryNum:0,
          lossNum:0,
        },
        // step 2
        form: {
          name: '',
          region: undefined,
          date1: undefined,
          delivery: false,
          type: [],
          resource: '',
          desc: '',
        },
        // spinning
        spinning:true,
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
        this.current = 0
        // 险情内容置空
        this.emergency= ''
        // 加载置true
        this.spinning=true
        this.emergencyUploadModal=true
      },
      //详情按钮
      clickEmergencyToShow(){

      },
      //input number
      onNumberChange(value){
      },
      //modal step change
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
        let urpApi = emergencyCompile.uploadPdf;
        let formData = new FormData();
        formData.append("multipartFiles", file);
        uploadAction(urpApi,formData).then((res)=>{
          if (res.success){
            console.log(res.result)
            this.emergency=res.result
            this.spinning=false
          }
        })
        this.$message.success(`${file.name} 上传成功.`);
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
    padding-top: 10px;
  }

  .steps-action {
    margin-top: 24px;
    text-align: right;
  }
</style>