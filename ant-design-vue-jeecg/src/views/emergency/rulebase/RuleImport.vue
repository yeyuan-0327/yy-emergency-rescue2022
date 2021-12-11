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
              <a-icon key="edit" type="edit" @click="editClick"/>
          </template>
          <a-card-meta title=".Jar接口" description="通过Jar链接引入规则">
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
            <a-icon key="edit" type="edit" @click="editClick"/>
          </template>
          <a-card-meta title=".Xls文件" description="通过Excel文件引入规则">
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
            <a-icon key="edit" type="edit" @click="editClick"/>
          </template>
          <a-card-meta title=".Drl文件" description="通过Drl文件引入规则">
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
        <a-form-model-item ref="name" label="Activity name" prop="name">
          <a-input
            v-model="form.name"
            @blur="
          () => {
            $refs.name.onFieldBlur();
          }
        "
          />
        </a-form-model-item>
        <a-form-model-item label="Activity zone" prop="region">
          <a-select v-model="form.region" placeholder="please select your zone">
            <a-select-option value="shanghai">
              Zone one
            </a-select-option>
            <a-select-option value="beijing">
              Zone two
            </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item label="Activity time" required prop="date1">
          <a-date-picker
            v-model="form.date1"
            show-time
            type="date"
            placeholder="Pick a date"
            style="width: 100%;"
          />
        </a-form-model-item>
        <a-form-model-item label="Instant delivery" prop="delivery">
          <a-switch v-model="form.delivery" />
        </a-form-model-item>
        <a-form-model-item label="Activity type" prop="type">
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
        <a-form-model-item label="Resources" prop="resource">
          <a-radio-group v-model="form.resource">
            <a-radio value="1">
              Sponsor
            </a-radio>
            <a-radio value="2">
              Venue
            </a-radio>
          </a-radio-group>
        </a-form-model-item>
        <a-form-model-item label="Activity form" prop="desc">
          <a-input v-model="form.desc" type="textarea" />
        </a-form-model-item>
        <a-form-model-item :wrapper-col="{ span: 14, offset: 4 }">
          <a-button type="primary" @click="onSubmit">
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
  import {getAction, postAction} from "@/api/manage";
  import { dataManageApi } from '@/api/EmergencyApi.js'

  export default {
    name: 'RuleImport',
    data () {
      return {
        ruleWriteModal:false,
        ruleWriteModalTitle:"",
        confirmLoading: false,
        ModalText:"xxxxx",
        //
        labelCol: { span: 4 },
        wrapperCol: { span: 14 },
        other: '',
        form: {
          name: '',
          region: undefined,
          date1: undefined,
          delivery: false,
          type: [],
          resource: '',
          desc: '',
        },
        rules: {
          name: [
            { required: true, message: 'Please input Activity name', trigger: 'blur' },
            { min: 3, max: 5, message: 'Length should be 3 to 5', trigger: 'blur' },
          ],
          region: [{ required: true, message: 'Please select Activity zone', trigger: 'change' }],
          date1: [{ required: true, message: 'Please pick a date', trigger: 'change' }],
          type: [
            {
              type: 'array',
              required: true,
              message: 'Please select at least one activity type',
              trigger: 'change',
            },
          ],
          resource: [
            { required: true, message: 'Please select activity resource', trigger: 'change' },
          ],
          desc: [{ required: true, message: 'Please input activity form', trigger: 'blur' }],
        },
      }
    },
    methods: {
      editClick(){
        this.ruleWriteModalTitle = ".Jar接口"
        this.ruleWriteModal = true
      },
      ruleWriteOk(e) {
        this.confirmLoading = true;
        setTimeout(() => {
          this.confirmLoading = false;
          this.ruleWriteModal = false
        }, 2000);
      },
      ruleWriteCancel(e) {
        console.log('Clicked cancel button');
        this.visible = false;
      },
      onSubmit() {
        this.$message.success(
          'This is a prompt message for success, and it will disappear in 10 seconds',
          3,
        );
        this.$refs.ruleForm.validate(valid => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm() {
        this.$refs.ruleForm.resetFields();
      },
    },
    created() {
    }
  }
</script>

<style scoped>

</style>