import Enum from "./Enum.js";

// settleTaskStatusEnum: new Enum()
//   .add("ALL", "全部", null)
//   .add("SETTLE", "待落户", 0)
//   .add("SETTLED", "已落户", 1)
//   .add("CANCEL", "已取消", 2);

// export default { settleTaskStatusEnum };


class enum_edge extends Enum {
    
    /**
     * 枚举对象
     */
    static NORMAL = [1, '正常'];
    static DISABLE = [0, '禁用'];
    
    /**
     * 状态编码
     */
    // static code;
    
    /**
     * 状态描述
     */
    // static desc;
    
}

const obj = new enum_edge()

export default obj
