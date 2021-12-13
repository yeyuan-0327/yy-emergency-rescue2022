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
        <a-form-model-item label="所属险情" prop="emergency_type">
          <a-select v-model="form.emergency_type" placeholder="请输入该规则的归属险情类别">
<!--        预留接口 可以从接口中获取到险情类别-->
            <a-select-option value="socialEmergency">
              社会动员
            </a-select-option>
            <a-select-option value="peopleSettlement">
              人员安置
            </a-select-option>
            <a-select-option value="peopleRescue">
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
              <a :href="url.downloadUrl" download="modal.xls">模版文件</a>
            </a-button>
          </a-space>
          <a-button v-show="ruleType==='Drl'" disabled>
            Drl类型
          </a-button>
        </a-form-model-item>
<!--        规则类型为Jar显示-->
        <a-form-model-item
          v-show="ruleType==='Jar'"
          ref="resource"  label="规则链接" prop="resource">
          <a-input-search @search="onRuleMetaSearch" v-model="form.resource"
                          @blur="() => {$refs.resource.onFieldBlur();}">
            <a-button v-if="form.resource === ''" slot="enterButton" type="primary" icon="search" disabled>
            </a-button>
            <a-button v-else slot="enterButton" type="primary" icon="search">
            </a-button>
          </a-input-search>
        </a-form-model-item>

<!--       规则类型为Excel Drl显示-->
        <a-form-model-item
          v-show="ruleType !== 'Jar'"
          ref="resource"  label="规则链接" prop="resource">
          <a-upload
            :action="uploadExcelUrl"
            :before-upload="handleBeforeUploadExcel"
            :multiple="true"
            :file-list="excelFileList"
            @change="handleUploadExcel"
            :showUploadList="{showRemoveIcon: true,showDownloadIcon: true}"
          >
            <a-button> <a-icon type="upload" /> Upload </a-button>
          </a-upload>
        </a-form-model-item>

        <a-form-model-item v-if="form.meta !== ''" label="规则详情" prop="meta" required>
          <a-input v-model="form.meta" type="textarea" disabled />
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
  import { dataManageApi } from '@/api/EmergencyApi.js'
  import AInputSearch from 'ant-design-vue/es/input/Search'
  import moment from 'moment'
  export default {
    name: 'RuleImport',
    components: { AInputSearch },
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
          emergency_type: undefined,
          invalid_date: undefined,
          resource: '',
          meta: ''
        },
        rules: {
          name: [
            { required: true, message: '请输入规则名称', trigger: 'blur' },
            { min: 2, max: 10, message: '长度应该在2到10之间', trigger: 'blur' },
          ],
          emergency_type: [{ required: true, message: '请选择所属险情类别', trigger: 'change' }],
          invalid_date: [{ required: true, message: '请选择失效时间', trigger: 'change' }],
          resource: [
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
        uploadExcelUrl: dataManageApi.ruleUploadExcel,
      }
    },
    methods: {
      moment,
      jarEditClick(){
        this.ruleWriteModalTitle = "Jar接口"
        this.ruleType = 'Jar';
        this.ruleWriteModal = true
        // 清空规则内容，使之不断重新加载
        this.form.meta = ''
      },
      excelEditClick(){
        this.ruleWriteModalTitle = "Excel文件"
        this.ruleType = 'Excel';
        this.ruleWriteModal = true
        // 清空规则内容，使之不断重新加载
        this.form.meta = ''
        // excel文件列表为空
        this.excelFileList = []
      },
      drlEditClick(){
        this.ruleWriteModalTitle = "Drl文件"
        this.ruleType = 'Drl';
        this.ruleWriteModal = true
        // 清空规则内容，使之不断重新加载
        this.form.meta = ''
        // excel文件列表为空
        this.excelFileList = []
      },
      // 当前日期之前无法选择
      disabledDate (current) {
        return current && current < moment().endOf('day')
      },
      // 传递表单
      postRuleForm(form){
        console.log(form)
        // let urlApi = "";
        // postAction(urlApi,form).then((res)=>{
        //   if (res.success){
        //   }else{}
        // })
        this.$message.success(
          '规则写入成功',
          2,
        );
        // 清空填写的规则
        this.resetForm()
      },
      // 确认按钮
      ruleWriteOk() {
        this.$refs.ruleForm.validate(valid => {
          if (valid) {
            this.form['type'] = this.ruleType
            // 调用post写入数据库
            this.postRuleForm(this.form)
            //规则写入loading动画
            this.confirmLoading = true;
            setTimeout(() => {
              this.confirmLoading = false;
              this.ruleWriteModal = false
            }, 2000);
          } else {
            this.$message.error(
              '请仔细检查，内容填写有误',
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
        // let urlApi = "";
        // let postList = [value]
        // postAction(url,postList).then((res)=>{
        //   if (res.success){
        //     this.rulesMeta = value;
        //   }
        // })
        this.form.meta = value
      },
      //验证按钮
      onRuleCheck() {
        this.$refs.ruleForm.validate(valid => {
          if (valid && !this.form.meta){
            this.$message.error(
              '请载入规则链接中的内容',
              2,
            );
          }
          else if (valid && this.form.meta) {
            this.$message.success(
              '验证成功，允许写入规则库',
              2,
            );
          } else {
            return false;
          }
        });
      },
      // 重置按钮
      resetForm() {
        this.$refs.ruleForm.resetFields();
      },
      // excel文件下载
      downloadExcelFile () {
        this.$message.warn('您点击了下载')
      },
      // excel文件上传
      handleBeforeUploadExcel(info){
        let formData = new FormData();
        formData.append("multipartFiles", info);
        uploadAction(this.uploadExcelUrl,formData).then((res)=>{
          if (res.success){
            console.log(res)
          }
        })
        const status = 'done';
        if (status === 'done') {
          this.$message.success(`${info.name} 文件上传成功.`);
          this.form.meta = "这是上传的规则文件内容"
        } else if (status === 'error') {
          this.$message.error(`${info.name} 文件上传失败.`);
        }
      },
      //文件改变时的操作
      handleUploadExcel(info) {
        // console.log(info)
        if (info.file.status=== 'removed'){
          //清空规则内容
          this.excelFileList = []
          this.form.meta = ''
        }
        else{
          this.excelFileList.push({
            uid: -1,
            name: info.file.name,
            status: 'done',
            url: '/file/insuranceInfoCheck.xls',
          },)
          let fileList = this.excelFileList;
          // 1. Limit the number of uploaded files
          //    Only to show two recent uploaded files, and old ones will be replaced by the new
          fileList = fileList.slice(-1);
          // // 2. read from response and show file link
          // fileList = fileList.map(file => {
          //   if (file.response) {
          //     // Component will show file.url as link
          //     file.url = file.response.url;
          //   }
          //   return file;
          // });
          //
          this.excelFileList = fileList;
        }
      },
    },
    created() {
    }
  }
</script>

<style >
  a {
    color: inherit;
  }
</style>