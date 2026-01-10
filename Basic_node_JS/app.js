function hello(name){
    console.log("hello" + " " + name);
}
hello("Abhay");

exports.hello = hello;
console.log(module);