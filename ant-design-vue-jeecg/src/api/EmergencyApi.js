// 基础数据 api
export const dataManageApi = {
  disableColumnOption : ["person_id", "person_name", "birth", "unit_social_credit_identifier", "unit_name", "person_phone",
  'address', 'bank_account', 'email','student_no','graduate_school','study_major','unified_social_credit_identifier',
  'enterprise_name','address_geom','legal_person_id','legal_person','phone','spare_resources_name','response_person','response_phone'
  ],
  apiClickDetailTable:'/datamanage/databaseInfo/clickDetailTable',
  apiSelectCharGroupByField:'/datamanage/databaseInfo/selectCharGroupByField',
  selectCharGroupByBirthField:'/datamanage/databaseInfo/selectCharGroupByBirthField',
  selectCharGroupBySexField: '/datamanage/databaseInfo/selectCharGroupByAnyField',
  fetchDimFactRelation:'/datamanage/databaseInfo/fetchDimFactRelation',
  fetchDwData:'/datamanage/databaseInfo/fetchDwData',
  factDataTable:'/datamanage/databaseInfo/factDataTable',
}

export const ruleBaseSet = {
  //Excel规则文件上传
  ruleUploadExcel:'/ruleSet/ruleCite/ruleUploadExcel',
  //Jar链接解析
  compileJarLink:'/ruleSet/ruleCite/compileJarLink',
  ruleUploadDB:'/ruleSet/ruleCite/ruleUploadDB',
  //获取rule列表
  getRuleList: '/ruleSet/ruleList/getRuleList',
  deleteRule: '/ruleSet/ruleList/deleteRule',
}

export const emergencyCompile={

}