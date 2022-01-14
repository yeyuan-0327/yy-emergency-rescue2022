<template>
  <div>
    <a-card >
      <a-row>
        <a-col :span="6">
          <a-cascader
            size="large"
            :options="options"
            :load-data="loadSelectData"
            placeholder="Please select"
            change-on-select
            style="width: 300px;margin-left: 20px"
            @change="onSelectChange"
          />
          <a-card style="min-height: 500px" :bordered="false">
            <a-list item-layout="horizontal"
                    :data-source="select_emergency_data">
              <a-list-item slot="renderItem" slot-scope="item, index">
                <a @click="similarRecommend(item.task_id)" slot="actions">相似</a>
                <a @click="ruleRecommend(item.task_id)" slot="actions">规则</a>
                <a-list-item-meta>
                  <span slot="title" >{{ item.task_name }}</span>
                </a-list-item-meta>
              </a-list-item>
            </a-list>
          </a-card>
        </a-col>
        <a-col :span="18">
          <a-card style="min-height: 300px" :bordered="!selectedTaskId">
            <a-table v-show="selectedTaskId && !ruleFlag"
                     :columns="recommend_task_columns"
                     :data-source="recommend_task_data"
                     :pagination="false"
                     rowKey="task_id"
                     :scroll="{ y: 220 }"
            >
              <span slot="tags" slot-scope="tags">
              <a-tag
                :color="tags > '70' ? 'volcano' : tags > '60' ? 'green':'geekblue'"
              >
                {{ tags.toUpperCase() }}%
              </a-tag>
              </span>
              <span slot="action" slot-scope="text, record">
                <a @click="recommendTaskDetail(record.task_id)">详情 </a>
                <a-divider type="vertical" />
                <a @click="changeTask(record.task_id)">更改 </a>
              </span>
            </a-table>
            <div v-show="ruleFlag">
              <a-row>
                <a-col :span="12">
                  <a-card title="适用规则" :bordered="false">
                    <a-card-grid
                      v-for="i in ruleList"
                      :key="i.id"
                      style="text-align:center"
                      @click="onRuleClick(i.id)">
                      {{i.name}}
                    </a-card-grid>
                  </a-card>
                </a-col>
                <a-col :span="12">
                  <div v-if="checkedRule" style="margin-left: 1px">
                    <a-card title="选用规则" :bordered="false" >
                      <a-radio-group v-model="ruleForm[checkedRule]===''?'':ruleForm[checkedRule]"
                                     @change="onSingleRuleChange"
                      >
                        <a-radio
                          v-for="rule in (ruleList[checkedRule-1]).metaList"
                          :key="rule.name"
                          :value = "rule.name"
                        >
                          {{rule.name}}
                        </a-radio>
                      </a-radio-group>
                    </a-card>
                  </div>
                  <div v-else style="text-align: center;margin-top: 20%">
                    <p>
                      点击左侧任一规则进行内容选用
                    </p>
                  </div>
                </a-col>
              </a-row>
            </div>
            <div v-show="!selectedTaskId" style="text-align: center;margin-top: 8%" >
              <p>
                点击左侧相似或规则以加载任务进行推荐
              </p>
              <p>
                相似推荐--相似程度的任务推荐；规则推荐--专家规则系统推荐
              </p>
            </div>
          </a-card>
          <a-card style="min-height: 300px" :bordered="!selectedTaskId">
<!--            -->
            <div v-show="recommendTaskId">
              <a-descriptions bordered  >
                <a-descriptions-item label="Product">
                  Cloud Database
                </a-descriptions-item>
                <a-descriptions-item label="Billing">
                  Prepaid
                </a-descriptions-item>
                <a-descriptions-item label="Time">
                  18:00:00
                </a-descriptions-item>
                <a-descriptions-item label="Amount">
                  $80.00
                </a-descriptions-item>
                <a-descriptions-item label="Discount">
                  $20.00
                </a-descriptions-item>
                <a-descriptions-item label="Official">
                  $60.00
                </a-descriptions-item>
                <a-descriptions-item label="Config Info">
                  Data disk type: MongoDB
                  <br />
                  Database version: 3.4
                  <br />
                  Package: dds.mongo.mid
                  <br />
                  Storage space: 10 GB
                  Replication factor: 3
                  Region: East China 1
                  <br/>
                </a-descriptions-item>
              </a-descriptions>
              <div class="button-action" >
                <a-button type="primary">应用</a-button>
              </div>
            </div>
<!--            -->
            <div v-show="!recommendTaskId & !ruleFlag" style="text-align: center;margin-top: 8%" >
              <p>
                点击上侧详情或更改以加载推荐任务
              </p>
              <p>
                详情--相似任务内容详情；更改--相似任务参数修改
              </p>
            </div>
<!--            -->
            <div v-show="ruleFlag" >
              <a-form-model :model="taskDetailForm" :label-col="labelCol" :wrapper-col="wrapperCol">
                <a-form-model-item
                  v-for="key in Object.keys(taskDetailForm)"
                  :key="key"
                  :label="key">
                  <a-input v-model="taskDetailForm[key]" />
                </a-form-model-item>
                <a-form-model-item label="规则列表">
                  <a-textarea disabled
                              v-model="JSON.stringify(ruleForm).replace(/null,|[[\\\]]/g,'')"
                              placeholder="Controlled autosize"
                              :auto-size="{ minRows: 3, maxRows: 5 }"
                  ></a-textarea>
                </a-form-model-item>
              </a-form-model>
              <div class="button-action">
                <a-space>
                  <a-button @click="clearTaskDetailForm">清空</a-button>
                  <a-button @click="useTaskDetailForm">应用</a-button>
                  <a-button type="primary" :loading="publishLoading" @click="publishTaskDetailForm">应用并发布</a-button>
                </a-space>
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
    <a-modal
      title="Title"
      :visible="popModalVisible"
      :confirm-loading="popModalConfirmLoading"
      @ok="popModalOk"
      @cancel="popModalCancel"
    >
      <p>123456</p>
    </a-modal>
  </div>
</template>

<script>
  const select_emergency_data = [
    {
      task_id:'1',
      task_name: 'Ant Design Title 1',
    },
    {
      task_id:'2',
      task_name: 'Ant Design Title 2',
    },
    {
      task_id:'3',
      task_name: 'Ant Design Title 3',
    },
    {
      task_id:'4',
      task_name: 'Ant Design Title 4',
    },
    {
      task_id:'5',
      task_name: 'Ant Design Title 1',
    },
    {
      task_id:'6',
      task_name: 'Ant Design Title 2',
    },
    {
      task_id:'7',
      task_name: 'Ant Design Title 3',
    },
    {
      task_id:'8',
      task_name: 'Ant Design Title 4',
    },
  ];
  const recommend_task_columns = [
    {
      title: '任务ID',
      dataIndex: 'task_id',
      key: 'task_id',
      width: 80,
    },
    {
      title: '任务名',
      dataIndex: 'task_name',
      key: 'task_name',
    },
    {
      title: '险情相似度',
      dataIndex: 'emergency_similar',
      key: 'address',
    },
    {
      title: '伤亡相似度',
      dataIndex: 'injury_death_similar',
      key: 'injury_death_similar',
    },
    {
      title: '地点相似度',
      dataIndex: 'address_similar',
      key: 'address_similar',
    },
    {
      title: '总体相似度',
      key: 'all_similar',
      dataIndex: 'all_similar',
      scopedSlots: { customRender: 'tags' },
    },
    {
      title: '操作',
      key: 'action',
      scopedSlots: { customRender: 'action' },
    },
  ];
  const recommend_task_data = [
    {
      task_id: '1',
      task_name: '相关险情1',
      emergency_similar: '18%',
      injury_death_similar: '50%',
      address_similar:'40%',
      all_similar: '77',
    },
    {
      task_id: '2',
      task_name: '相关险情2',
      emergency_similar: '20%',
      injury_death_similar: '20%',
      address_similar:'21%',
      all_similar: '66',
    },
    {
      task_id: '3',
      task_name: '相关险情3',
      emergency_similar: '43%',
      injury_death_similar: '22%',
      address_similar:'64%',
      all_similar: '55',
    },
    {
      task_id: '4',
      task_name: '相关险情1',
      emergency_similar: '18%',
      injury_death_similar: '50%',
      address_similar:'40%',
      all_similar: '77',
    },
    {
      task_id: '5',
      task_name: '相关险情2',
      emergency_similar: '20%',
      injury_death_similar: '20%',
      address_similar:'21%',
      all_similar: '66',
    },
    {
      task_id: '6',
      task_name: '相关险情3',
      emergency_similar: '43%',
      injury_death_similar: '22%',
      address_similar:'64%',
      all_similar: '55',
    },
  ];
  export default {
    name: 'TaskManage',
    data(){
      return {
        options: [
          {
            value: 'zhejiang',
            label: 'Zhejiang',
            isLeaf: false,
          },
          {
            value: 'jiangsu',
            label: 'Jiangsu',
            isLeaf: false,
          },
        ],
        //list
        select_emergency_data,
        //selectedTask
        selectedTaskId:'',
        recommendTaskId:'',
        ruleFlag:false,
        //table
        recommend_task_data,
        recommend_task_columns,
        // rule表
        ruleList:[
          {
          id:'1',
          name:'年龄优先',
          metaList:[{
            name:'18-25优先',
          },{
            name:'25-30优先',
          },{
            name:'30-35优先',
          },{
            name:'35以上优先',
          },]
        },
          {
          id:'2',
          name:'血型优先',
          metaList:[{
            name:'O优先',
          },{
            name:'A优先',
          },{
            name:'B优先',
          },{
            name:'AB优先',
          },]
        },{
          id:'3',
          name:'党员优先'
        },{
          id:'4',
          name:'人才优先'
        },{
          id:'5',
          name:'距离优先'
        },{
          id:'6',
          name:'学历优先'
        },{
          id:'7',
          name:'身高优先'
        },
        ],
        checkedRule:undefined,
        ruleForm:[],
        // form modal
        labelCol: { span: 2 },
        wrapperCol: { span: 20 },
        taskDetailForm: {
          name1: 'abcd',
          name2: 'abcd',
          name3: 'abcd',
        },
        // pop modal
        popModalVisible: false,
        popModalConfirmLoading: false,
        publishLoading:false,
      };
    },
    methods:{
      // 选择框改变
      onSelectChange(value) {
        console.log(value)
      },
      // 动态加载选择框数据
      loadSelectData(selectedOptions) {
        const targetOption = selectedOptions[selectedOptions.length - 1];
        targetOption.loading = true;

        // load options lazily
        setTimeout(() => {
          targetOption.loading = false;
          targetOption.children = [
            {
              label: `${targetOption.label} Dynamic 1`,
              value: 'dynamic1',
            },
            {
              label: `${targetOption.label} Dynamic 2`,
              value: 'dynamic2',
            },
          ];
          this.options = [...this.options];
        }, 1000);
      },
      //相似推荐
      similarRecommend(task_id){
        this.clearAllInfo()
        this.selectedTaskId = task_id
        this.ruleFlag=false
      },
      //详情相似推荐的任务
      recommendTaskDetail(task_id){
        this.recommendTaskId=task_id
        console.log(task_id)
      },
      //更改相似推荐的任务
      changeTask(task_id){
        this.recommendTaskId=task_id
        console.log(task_id)
      },
      //规则推荐
      ruleRecommend(task_id){
        this.clearAllInfo()
        this.selectedTaskId = task_id
        this.ruleFlag=true
      },
      //规则选用
      onRuleClick(checkedValues) {
        this.checkedRule=Number(checkedValues)
      },
      //选用某一详细规则
      onSingleRuleChange(e) {
        this.ruleForm[this.checkedRule] = e.target.value
      },
      //应用button
      useTaskDetailForm(){
        this.showPopModal()
      },
      //应用并发布button
      publishTaskDetailForm(){
        this.publishLoading=true
        setTimeout(() => {
          this.publishLoading=false
        }, 1000);
      },
      //清空button
      clearTaskDetailForm(){
        this.taskDetailForm = {
            name1: '',
            name2: '',
            name3: '',
        }
        this.ruleForm = []
      },
      //clear all
      clearAllInfo(){
        this.selectedTaskId = ''
        this.recommendTaskId = ''
        this.checkedRule = ''
        this.ruleForm = []
      },
      // pop modal
      showPopModal() {
        this.popModalVisible = true;
      },
      popModalOk(e) {
        this.popModalConfirmLoading = true;
        setTimeout(() => {
          this.popModalVisible = false;
          this.popModalConfirmLoading = false;
        }, 1000);
      },
      popModalCancel(e) {
        console.log('Clicked cancel button');
        this.popModalVisible = false;
      },
      // singleRule
      handleChange(value) {
        console.log(`selected ${value}`);
      },
    }
  }
</script>

<style scoped>
  .button-action {
    margin-top: 24px;
    text-align: right;
  }
</style>