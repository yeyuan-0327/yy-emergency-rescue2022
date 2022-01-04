<template>
  <a-card style="height: 650px">
    <a-page-header
      title="规则库引用方法">
      <br/>
      <a-space :size="250">
<!--        jar接口-->
        <a-card hoverable style="width: 250px">
          <img
            slot="cover"
            alt="droolsExample"
            src="@/assets/drools.png"
          />
          <template slot="actions" class="ant-card-actions">
              <a-icon key="edit" type="edit" @click="jarEditClick"/>
          </template>
          <a-card-meta title="Jar接口" description="通过Jar链接引入规则">
          </a-card-meta>
        </a-card>
<!--        xls文件-->
        <a-card hoverable style="width: 250px">
          <img
            slot="cover"
            alt="excelExample"
            src="@/assets/excel.png"
          />
          <template slot="actions" class="ant-card-actions">
            <a-icon key="edit" type="edit" @click="excelEditClick"/>
          </template>
          <a-card-meta title="Excel文件" description="通过Excel文件引入规则">
          </a-card-meta>
        </a-card>
<!--        drl文件-->
        <a-card hoverable style="width: 250px">
          <img
            slot="cover"
            alt="fileExample"
            src="@/assets/file.png"
          />
          <template slot="actions" class="ant-card-actions">
            <a-icon key="edit" type="edit" @click="drlEditClick"/>
          </template>
          <a-card-meta title="Drl文件" description="通过Drl文件引入规则">
          </a-card-meta>
        </a-card>
      </a-space>
    </a-page-header>
    <a-modal v-model="ruleWriteModal"
             :title="ruleWriteModalTitle"
             :confirm-loading="confirmLoading"
             switchFullscreen
             :width="1000"
             @ok="ruleWriteOk"
             @cancel="ruleWriteCancel">
      <a-form-model
        ref="ruleForm"
        :model="form"
        :rules="rules"
        :label-col="labelCol"
        :wrapper-col="wrapperCol"
      >
        <a-form-model-item ref="name" label="规则名称" prop="name">
          <a-input
            v-model="form.name"
            @blur="
          () => {
            $refs.name.onFieldBlur();
          }
        "
          />
        </a-form-model-item>
        <a-form-model-item label="所属任务" prop="task_type">
          <a-select v-model="form.task_type" placeholder="请输入该规则的归属任务类别">
<!--        预留接口 可以从接口中获取到任务类别-->
            <a-select-option value="社会动员">
              社会动员
            </a-select-option>
            <a-select-option value="人员安置">
              人员安置
            </a-select-option>
            <a-select-option value="人员搜救">
              人员搜救
            </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item label="失效时间" required prop="invalid_date">
          <a-date-picker
            v-model="form.invalid_date"
            type="date"
            placeholder="创建规则成功后则生效"
            style="width: 100%;"
            :disabledDate="disabledDate"
          />
        </a-form-model-item>
        <a-form-model-item label="规则类型" >
          <a-button v-show="ruleType==='Jar'" disabled>
            Jar类型
          </a-button>
          <a-space v-show="ruleType==='Excel'">
            <a-button  disabled>
              Excel类型
            </a-button>
            <a-button @click="downloadExcelFile">
              <a-icon type="download" />
              <a :href="url.downloadUrl" download="modal.xls" style="color: inherit;">模版文件</a>
            </a-button>
          </a-space>
          <a-button v-show="ruleType==='Drl'" disabled>
            Drl类型
          </a-button>
        </a-form-model-item>
<!--        规则类型为Jar显示-->
        <a-form-model-item
          v-show="ruleType==='Jar'"
          ref="path"  label="规则链接" prop="path">
          <a-input-search @search="onRuleMetaSearch" v-model="form.path"
                          @blur="() => {$refs.path.onFieldBlur();}">
            <a-button v-if="form.path === ''" slot="enterButton" type="primary" icon="search" disabled>
            </a-button>
            <a-button v-else slot="enterButton" type="primary" icon="search">
            </a-button>
          </a-input-search>
        </a-form-model-item>

<!--       规则类型为Excel Drl显示-->
        <a-form-model-item
          v-show="ruleType !== 'Jar'"
          ref="path"  label="规则链接" prop="path">
          <a-upload
            :action="uploadExcelUrl"
            :multiple="true"
            :file-list="excelFileList"
            @change="handleUploadExcel"
            :showUploadList="{showRemoveIcon: true,showDownloadIcon: true}"
          >
            <a-button> <a-icon type="upload" /> 文件上传 </a-button>
          </a-upload>
        </a-form-model-item>

        <a-form-model-item v-if="form.meta !== ''" label="规则详情" required prop="meta">
          <a-textarea v-model="form.meta" :auto-size="{ minRows: 2, maxRows: 6 }" disabled />
        </a-form-model-item>

        <a-form-model-item :wrapper-col="{ span: 14, offset: 4 }">
          <a-button @click="onRuleCheck" >
            验证
          </a-button>
          <a-button style="margin-left: 10px;" @click="resetForm">
            重置
          </a-button>
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </a-card>
</template>

<script>
  import {getAction, postAction,uploadAction} from "@/api/manage";
  import { ruleBaseSet } from '@/api/EmergencyApi.js'
  import AInputSearch from 'ant-design-vue/es/input/Search'
  import moment from 'moment'
  import ATextarea from 'ant-design-vue/es/input/TextArea'

  export default {
    name: 'RuleImport',
    components: { ATextarea, AInputSearch },
    data () {
      return {
        ruleWriteModal:false,
        ruleWriteModalTitle:"",
        confirmLoading: false,
        //
        labelCol: { span: 4 },
        wrapperCol: { span: 14 },
        other: '',
        // 规则类型
        ruleType: '',
        form: {
          name: '',
          task_type: undefined,
          invalid_date: undefined,
          path: '',
          meta: ''
        },
        rules: {
          name: [
            { required: true, message: '请输入规则名称', trigger: 'blur' },
            { min: 2, max: 20, message: '长度应该在2到20之间', trigger: 'blur' },
          ],
          task_type: [{ required: true, message: '请选择所属任务类别', trigger: 'change' }],
          invalid_date: [{ required: true, message: '请选择失效时间', trigger: 'change' }],
          path: [
            { required: true, message: '请引入规则链接', trigger: 'blur' },
          ],
          meta: [
            { required: true, message: '请点击搜索按钮', trigger: 'blur' },
          ],
        },
        // excel模版文件
        url: {
          downloadUrl: '/file/insuranceInfoCheck.xls',
        },
        // excel文件上传
        excelFileList: [],
        uploadExcelUrl: ruleBaseSet.ruleUploadExcel,
      }
    },
    methods: {
      moment,
      jarEditClick(){
        this.ruleWriteModalTitle = "Jar接口"
        this.ruleType = 'Jar';
        this.ruleWriteModal = true
        // 清空内容，使之不断重新加载
        this.resetForm()
      },
      excelEditClick(){
        this.ruleWriteModalTitle = "Excel文件"
        this.ruleType = 'Excel';
        this.ruleWriteModal = true
        // 清空内容，使之不断重新加载
        this.resetForm()
      },
      drlEditClick(){
        this.ruleWriteModalTitle = "Drl文件"
        this.ruleType = 'Drl';
        this.ruleWriteModal = true
        // 清空内容，使之不断重新加载
        this.resetForm()
      },
      // 当前日期之前无法选择
      disabledDate (current) {
        return current && current < moment().endOf('day')
      },
      // 传递表单
      postRuleForm(form){
        console.log(form)
        //确认按钮 loading动画
        this.confirmLoading = true;
        // 调用api
        let urlApi = ruleBaseSet.ruleUploadDB;
        postAction(urlApi,form).then((res)=>{
          if (res.success){
            console.log(res.result)
            this.$message.success('规则写入成功',2);
            this.ruleWriteModal = false
          }
          else this.$message.error('服务器原因，上传失败',2);
          this.confirmLoading = false;
        })
      },
      // 确认按钮
      ruleWriteOk() {
        this.$refs.ruleForm.validate(valid => {
          if (valid && this.form.meta) {
            this.form['type'] = this.ruleType
            // 调用post写入数据库
            this.postRuleForm(this.form)
          } else {
            this.$message.error(
              '请检查，内容有误或未载入规则链接中的内容',
              2,
            );
            return false;
          }
        });
      },
      ruleWriteCancel(e) {
        console.log('Clicked cancel button');
        this.visible = false;
      },
      // jar链接搜索按钮
      onRuleMetaSearch(value){
        // 获取规则内容api
        let urlApi = ruleBaseSet.compileJarLink;
        let postList = [value]
        postAction(urlApi,postList).then((res)=>{
          if (res.success){
            let meta = '';
            _(res.result).forEach(function(value,key) {
              if (key!==0) meta += key + ".";
              meta += value;
              meta += '\n';
            })
            this.form.meta = meta
          }
          else this.$message.error('请仔细检查规则链接，内容无法解析',2);
        })
      },
      //验证按钮
      onRuleCheck() {
        this.$refs.ruleForm.validate(valid => {
          if (valid && this.form.meta) {
            this.$message.success('验证成功，允许写入规则库',2);
          } else {
            this.$message.error('请检查，内容有误或未载入规则链接中的内容',2);
            return false;
          }
        });
      },
      // 重置按钮
      resetForm() {
        this.form.meta = ''
        this.excelFileList = []
        this.$nextTick(()=> {
          this.$refs.ruleForm.resetFields();
        })
      },
      // excel文件下载
      downloadExcelFile () {
        this.$message.warn('您点击了下载')
      },
      // excel文件上传
      uploadExcel(file){
        console.log(file)
        let formData = new FormData();
        formData.append("multipartFiles", file);
        // 文件上传api
        uploadAction(this.uploadExcelUrl,formData).then((res)=>{
          if (res.success){
            this.excelFileList.push({
              uid: file.uid,
              name: file.name,
              status: 'done',
              url: '/file/' + file.name,
            },)
            let fileList = this.excelFileList;
            // 1. Limit the number of uploaded files
            //    Only to show two recent uploaded files, and old ones will be replaced by the new
            fileList = fileList.slice(-1);
            this.excelFileList = fileList;
            this.$message.success(`${file.name} 文件上传成功.`);
            this.form.path = res.result;
            this.form.meta = "这是上传的Excel规则文件内容"
          }
          else{
            this.$message.error(`${file.name} 文件上传失败.`);
          }
        })
      },
      //文件改变时的操作
      handleUploadExcel(info) {
        if (info.file.status=== 'removed'){
          //清空规则内容
          this.excelFileList = []
          this.form.meta = ''
        }
        else{
          // 上传excel文件
          this.uploadExcel(info.file.originFileObj)
        }
      },
    },
    created() {
    }
  }
</script>

<style >
  /*a {*/
  /*  color: inherit;*/
  /*}*/
</style>