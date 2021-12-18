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
          <!--            <a-card v-for="task in task_list" :key="task.name"-->
          <!--                    hoverable-->
          <!--                    style="height: 150px;width: 150px">-->
          <!--              <img-->
          <!--                style="margin-top: -10px;margin-left: 5px"-->
          <!--                alt="task"-->
          <!--                src="@/assets/task.png"-->
          <!--              />-->
          <!--              <a-card-meta :title="task.name" style="margin-top: 10px;margin-left: 15px">-->
          <!--              </a-card-meta>-->
          <!--            </a-card>-->
        </a-space>
      </a-tab-pane>
    </a-tabs>
    <a-modal v-model="taskCreateModal"
             :title="taskCreateModalTitle"
             switchFullscreen
             okText="创建"
             @ok="onTaskSubmit"
             @cancel="onTaskCancel"
             :width="1000">
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
    </a-modal>
  </div>
</template>

<script>
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
            name:"使用企业资源",
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
        form: {
          name: '',
          region: undefined,
          date1: undefined,
          delivery: false,
          type: [],
          resource: '',
          desc: '',
        },
      };
    },
    methods: {
      taskClick(record){
        this.taskCreateModal=true
        this.taskCreateModalTitle=record[0].name
        console.log("点击了任务创建")
      },
      onTaskSubmit() {
        this.$message.success('任务创建成功!')
        this.taskCreateModal=false
      },
      onTaskCancel() {
        this.taskCreateModal=false
      },
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