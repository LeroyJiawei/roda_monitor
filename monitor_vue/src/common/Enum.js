

const _flag = Symbol('flag')
export default class Enum {
    /**
     * 添加枚举字段
     * field: 枚举字段
     * label: 界面显示
     * value: 枚举值
     */
    constructor(flag) {
        if(flag != undefined && flag == _flag){
            return;
        }
        //获取所有的成员变量
        let objList = this.__proto__.constructor
        //用来装载枚举类型与变量值
        let enumList = [];
        let infoList = [];
        //遍历
        for(let obj in objList){
            //判断对象是否为Array类型，把数组和值进行分离
            if(objList[obj] instanceof Array){
                enumList.push(obj)
            }else {
                infoList.push(obj)
            }
        }
        //创建所有的枚举对象
        for (let i = 0; i < enumList.length; i++) {
            //枚举对象数组值
            let enumObj = objList[enumList[i]]
            //判断数组值是否与变量长度匹配，不匹配直接抛出异常
            if(enumObj.length != infoList.length){
                throw new Error(enumList[i] +' 对象实例化失败:枚举参数不匹配')
            }
            //创建枚举对象，使用falg标志防止重复创建
            let obj = new Enum(_flag)
            //设置枚举值
            for (let x = 0; x < infoList.length; x++) {
                obj[infoList[x]] = enumObj[x]
            }
            //挂载到this上
            console.log(enumList[i])
            this[enumList[i]] = obj
        }
        //防止被修改
        Object.freeze(this)
    }

    // add (field, label, value) {
    //   this[field] = {label, value}
    //   return this
    // }
  
    // /**
    //  * 根据枚举value获取其label
    //  */
    // getLabelByValue (value) {
    //   // 字段不存在返回‘’
    //   if (value === undefined || value === null) {
    //     return ''
    //   }
    //   for (let i in this) {
    //     let e = this[i]
    //     if (e && e.value === value) {
    //       return e.label
    //     }
    //   }
  
    //   return ''
    // }
  }

