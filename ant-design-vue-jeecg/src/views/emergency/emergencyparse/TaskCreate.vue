<template>
  <div class="card-container" >
    <a-tabs type="card" >
      <a-tab-pane v-for="dw in dw_list" :key="dw.key" :tab="dw.name">
        <a-space :size="150" >
          <div v-for="i in dw.task_list.length" :key="i">
            <a-card v-for="j in 2" :key="j"
                    v-if="(i-1)*2+j <= dw.task_list.length"
                    hoverable @click="taskClick(dw.task_list.slice((i-1)*2+j-1,(i-1)*2+j))"
                    style="height: 150px;width: 150px;margin-top: 20px">
              <img
                v-if="(i-1)*2+j <= dw.task_list.length"
                style="margin-top: -10px;margin-left: 5px"
                alt="task"
                src="@/assets/task.png"
              />
              <a-card-meta
                v-if="(i-1)*2+j <= dw.task_list.length"
                v-for="x in dw.task_list.slice((i-1)*2+j-1,(i-1)*2+j)"
                :key="x.name"
                :title="x.name" style="margin-top: 10px;margin-left: 15px">
              </a-card-meta>
            </a-card>
          </div>
        </a-space>
      </a-tab-pane>
    </a-tabs>
    <a-modal v-model="taskCreateModal"
             :title="taskCreateModalTitle"
             switchFullscreen
             okText="创建"
             @ok="onSubmit"
             @cancel="onTaskCancel"
             :width="1000">
      <a-form-model
        ref="taskForm"
        :model="task"
        :rules="rules"
        :label-col="labelCol"
        :wrapper-col="wrapperCol"
      >
        <a-form-model-item ref="name" label="任务名称" prop="name">
          <a-input
            v-model="task.name"
            @blur="
          () => {
            $refs.name.onFieldBlur();
          }
        "
          />
        </a-form-model-item>
        <a-form-model-item label="所属险情类型" prop="emergency_type">
          <a-checkbox-group v-model="task.emergency_type" @change="emergencyTypeCheckBox">
            <a-checkbox value="自然灾害" name="emergency_type">
                自然灾害
            </a-checkbox>
            <a-checkbox value="事故灾难" name="emergency_type">
                事故灾难
            </a-checkbox>
            <a-checkbox value="公共卫生事件" name="emergency_type">
                公共卫生事件
            </a-checkbox>
            <a-checkbox value="社会安全事件" name="emergency_type">
                社会安全事件
            </a-checkbox>
          </a-checkbox-group>
        </a-form-model-item>
        <a-form-model-item label="险情名称" prop="emergency_id">
          <a-select v-model="task.emergency" @select="emergencyIdSelect">
            <a-select-option
              v-for="e in emergencySelectList"
              :key = "e.id"
              :value="e">
              {{e.name}}
            </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item label="上传时间">
          <a-date-picker :value="moment(emergency.time, 'YYYY-MM-DD')" disabled>
          </a-date-picker>
          <span style="margin-left: 20px">险情等级:</span>
          <a-button
            type="dashed" disabled style="margin-left: 10px;margin-top: 3px">{{emergency.emergencyLevel}}</a-button>
        </a-form-model-item>
        <a-form-model-item label="险情发生地点" >
          <a-input v-model="emergency.address" disabled/>
        </a-form-model-item>
        <a-form-model-item label="险情内容">
          <a-input v-model="emergency.content" :auto-size="{ minRows: 5 }" type="textarea" disabled/>
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import moment from 'moment';
  import {getAction, postAction,uploadAction} from "@/api/manage";
  import { emergencyCompile } from '@/api/EmergencyApi.js'

  export default {
    name: 'TaskCreate',
    data() {
      return {
        dw_list:[
          {
            key:1,
            name:"使用人力资源",
            task_list:[
              {
                name : '社会动员'},
              {
                name : '治安维护'},
              {
                name : '医疗救护'},
              {
                name : '卫生防疫'},
              {
                name : '专业人才'},
              {
                name : '紧急驾驶'},
            ]
          },
          {
            key:2,
            name:"使用企业资源",
            task_list:[
              {
                name : '物资保障'},
              {
                name : '重型设备'},
              {
                name : '饮食保障'},
              {
                name : '紧急运输'},
            ]
          },
          {
            key:3,
            name:"使用其他资源",
            task_list:[
              {
                name : '人员搜救'},
              {
                name : '人员庇护'},
              {
                name : '应急队伍'},
              {
                name : '设备抢修'},
            ]
          },
        ],
        //modal
        taskCreateModal:false,
        taskCreateModalTitle:"",
        //form modal
        labelCol: { span: 4 },
        wrapperCol: { span: 14 },
        task: {
          name: '',
          emergency_type: [],
          emergency:'',
          emergency_id:'',
        },
        rules: {
          name: [
            { required: true, message: '请输入任务名称', trigger: 'blur' },
            { min: 4, max: 20, message: '长度应该为4到20', trigger: 'blur' },
          ],
          emergency: [{ required: true, message: '请选择所属险情', trigger: 'change' }],
          emergency_type: [
            {
              type: 'array',
              required: true,
              message: '请选择一项所属险情类型',
              trigger: 'change',
            },
          ],
        },
        emergency:{
          id:'',
          name:'',
          time: moment(),
          emergencyLevel:'',
          address:'',
          content:''
        },
        emergencySelectList:[],
        moment,
      };
    },
    methods: {
      taskClick(record){
        this.taskCreateModal=true
        this.taskCreateModalTitle=record[0].name
        // clear all
        this.clearData()
        this.task.name=record[0].name
      },
      //多选框单选
      emergencyTypeCheckBox(){
        // 清空单选框选项内容 重新读取
        this.task.emergency_id=''
        // 多选框单选
        this.task.emergency_type = [this.task.emergency_type[this.task.emergency_type.length-1]]
        // 加载单选框内容
        let apiUrl = emergencyCompile.getEmergencyByType
        postAction(apiUrl,this.task.emergency_type).then((res)=>{
          if (res.success){
            this.emergencySelectList=res.result
          }
        })
      },
      //
      emergencyIdSelect(value){
        let apiUrl = emergencyCompile.getEmergencyById
        this.task.emergency_id=value.id
        let postList = [value.id]
        postAction(apiUrl, postList).then((res)=>{
          if (res.success){
            this.emergency=res.result
          }
        })
      },
      //创建任务
      writeTask(){
        let apiUrl = emergencyCompile.writeTask
        let post = this.task
        postAction(apiUrl,post).then((res)=>{
          if (res.success){
            this.$message.success('任务创建成功!')
            this.taskCreateModal=false
          }
        })
      },
      // ok button
      onSubmit() {
        this.$refs.taskForm.validate(valid => {
          if (valid) {
            this.writeTask()
          } else {
            this.$message.error('任务创建失败，服务器原因!')
            return false;
          }
        });
      },
      onTaskCancel() {
        this.taskCreateModal=false
      },
      clearData(){
        this.task={
          name: '',
          emergency_type: [],
          emergency_id:'',
        }
        this.emergencySelectList=''
        this.emergency = {}
      }
    },
  };
</script>

<style scoped>
  .card-container {
    overflow: hidden;
    padding: 24px;
    min-height: 650px;
  }
  .card-container > .ant-tabs-card > .ant-tabs-content {
    min-height: 120px;
    margin-top: -16px;
  }

  .card-container > .ant-tabs-card > .ant-tabs-content > .ant-tabs-tabpane {
    background: #fff;
    padding: 24px;

  }

</style>