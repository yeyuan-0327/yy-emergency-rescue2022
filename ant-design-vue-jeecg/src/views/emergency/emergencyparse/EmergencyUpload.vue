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
      :columns="emergencyColumns"
      :dataSource="emergencyDataSource"
      :pagination="paginationOpt"
      :loading="loading"
      class="j-table-force-nowrap">
      <span slot="emergency_level"
            slot-scope="tag">
        <a-tag
          :key="tag"
          :color="tag === 1 ? 'red' : tag === 2 ? 'orange' : tag === 3? 'yellow':'blue'"
        >
        {{ tag }}
      </a-tag>
      </span>
      <span slot="task_list" slot-scope="tags">
      <a-tag
        v-for="tag in tags"
        :key="tag"
        :color="tag === 'loser' ? 'volcano' : tag.length > 5 ? 'geekblue' : 'green'"
      >
        {{ tag.substring(0,1) }}
      </a-tag>
    </span>
      <span slot="action" slot-scope="text, record">
        <a @click="clickEmergencyToShow(record)">详情</a>
      </span>
    </a-table>
    <!-- 弹框区域  -->
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
          <a-spin :spinning="emergency.spinning">
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
          <a-spin :spinning="compileEmergency.spinning">
            <a-form-model :model="compileEmergency" :label-col="labelCol" :wrapper-col="wrapperCol">
              <a-form-model-item label="险情名称">
                <a-input v-model="compileEmergency.name" disabled/>
              </a-form-model-item>
              <a-form-model-item label="险情类别">
                <a-select v-model="compileEmergency.emergencyType" placeholder="请选择险情类别" disabled>
                  <a-select-option value="自然灾害" >
                    自然灾害
                  </a-select-option>
                  <a-select-option value="事故灾害">
                    事故灾害
                  </a-select-option>
                </a-select>
              </a-form-model-item>
              <a-form-model-item label="上传时间">
                <a-date-picker :value="moment(compileEmergency.time, 'YYYY-MM-DD')" disabled>
                </a-date-picker>
                <span style="margin-left: 20px">险情等级:</span>
                <a-button type="dashed" disabled style="margin-left: 10px">{{compileEmergency.emergencyLevel}}级</a-button>
              </a-form-model-item>
              <a-form-model-item label="险情发生地点" >
                <a-input v-model="compileEmergency.address" disabled/>
              </a-form-model-item>
              <a-form-model-item label="分配子任务方式">
                <a-radio-group v-model="compileEmergency.taskAllocation">
                  <a-radio value="系统推荐">
                    系统推荐
                  </a-radio>
                  <a-radio value="人工选择">
                    人工选择
                  </a-radio>
                </a-radio-group>
              </a-form-model-item>
              <a-form-model-item label="相关子任务">
                <a-checkbox-group v-if="compileEmergency.taskAllocation === '系统推荐'" v-model="compileEmergency.taskList" disabled>
                  <a-row>
                    <a-col span="4" v-for="i in task_list" :key="i.task_name" >
                      <a-checkbox :value="i.task_name" name="task" >
                        {{i.task_name}}
                      </a-checkbox>
                    </a-col>
                  </a-row>
                </a-checkbox-group>
                <a-checkbox-group v-else v-model="compileEmergency.taskList">
                  <a-row>
                    <a-col span="4" v-for="i in task_list" :key="i.task_name" >
                      <a-checkbox :value="i.task_name" name="task" >
                        {{i.task_name}}
                      </a-checkbox>
                    </a-col>
                  </a-row>
                </a-checkbox-group>
              </a-form-model-item>

            </a-form-model>
          </a-spin>
        </div>
        <!--步骤按钮-->
        <div class="steps-action" >
          <a-button v-if="current > 0" style="margin-right: 8px" @click="prevStep">
            上一步
          </a-button>
          <a-button v-if="current < steps.length - 1 && current !== 0" type="primary" @click="nextStep">
            下一步
          </a-button>
          <a-button v-if="current === 0" type="primary" @click="nextStep" disabled>
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
  import moment from 'moment';
  import ACol from 'ant-design-vue/es/grid/Col'

  export default {
    name: 'EmergencyUpload',
    components: { ACol },
    data() {
      return {
        //搜索框
        searchEmergencyName:'',
        selectedRowKeys:[],
        //表格
        emergencyColumns:[
          {
            title: 'ID',
            dataIndex: 'id',
            align:"center",
          },
          {
            title: '险情名称',
            align:"center",
            dataIndex: 'name',
          },
          {
            title: '险情类别',
            align:"center",
            dataIndex: 'emergency_type',
          },
          {
            title: '险情等级',
            align:"center",
            dataIndex: 'emergency_level',
            scopedSlots: {customRender: 'emergency_level'},
          },
          {
            title: '发布时间',
            align:"center",
            dataIndex: 'time',
          },
          {
            title: '子任务',
            align:"center",
            dataIndex: 'task_list',
            scopedSlots: {customRender: 'task_list'},
          },
          {
            title: '操作',
            dataIndex: 'action',
            align:"center",
            fixed:"right",
            width:100,
            scopedSlots: { customRender: 'action' }
          }
        ],
        emergencyDataSource:[],
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
          spinning:true,
        },
        // step 2
        compileEmergency: {
          name: '',
          emergencyType: undefined,
          time: moment(),
          emergencyLevel:'',
          taskList: [],
          taskAllocation: '',
          address:'',
          spinning:true,
        },
        // date
        moment,
        // task api
        task_list:[
          {
            task_name : '社会动员'},
          {
            task_name : '治安维护'},
          {
            task_name : '医疗救护'},
          {
            task_name : '卫生防疫'},
          {
            task_name : '专业人才'},
          {
            task_name : '紧急驾驶'},
          {
            task_name : '物资保障'},
          {
            task_name : '重型设备'},
          {
            task_name : '饮食保障'},
          {
            task_name : '紧急运输'},
          {
            task_name : '人员搜救'},
          {
            task_name : '人员庇护'},
          {
            task_name : '应急队伍'},
          {
            task_name : '设备抢修'},
        ],
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
    created(){
      this.initEmergencyList()
    },
    methods: {
      initEmergencyList(){
        let apiUrl = emergencyCompile.emergencyList
        getAction(apiUrl).then((res)=>{
          if (res.success){
            this.emergencyDataSource = res.result
          }
        })
      },
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
        if (this.current === 2 && this.emergency.name !== '')this.compileEmergencyLevelTask();
      },
      prevStep() {
        this.current--;
      },
      clickDone(){
        let apiUrl = emergencyCompile.confirmEmergencyTaskPublish
        let postList = this.compileEmergency
        postAction(apiUrl,postList).then((res)=>{
          if (res.success){
            this.initEmergencyList();
          }
        })
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
            this.emergency = res.result
            this.emergency.spinning = false
          }
        })
        this.$message.success(`${file.name} 上传成功.`);
        this.current += 1
        return true
      },
      //vocal
      recordVocal(){
        this.emergencyUploadModal=false
        console.log('点击录音')
      },
      compileEmergencyLevelTask() {
        let apiUrl = emergencyCompile.ruleFireLevelTask
        let postList = this.emergency
        postAction(apiUrl,postList).then((res)=>{
          if (res.success){
            this.compileEmergency=res.result;
            this.compileEmergency.spinning=false;
          }
        })
      }
    },
  }
</script>

<style scoped>
  .steps-content {
    margin-top: 30px;
    border: 1px dashed #e9e9e9;
    border-radius: 6px;
    min-height: 300px;
    padding-top: 10px;
  }

  .steps-action {
    margin-top: 24px;
    text-align: right;
  }
</style>