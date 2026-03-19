const { makeBadge } = require("badge-maker");
const fs = require("node:fs");

function SPEC0() {
    const format = {
        label: 'SPEC',  // (Optional) Badge label
        message: '0',  // (Required) Badge message
        labelColor: '#555',  // (Optional) Label color
        color: '#4c1',  // (Optional) Message color
    }
    const badgeString = makeBadge(format);
    fs.writeFile("spec0.svg", badgeString, e => {
        if (e != null) {
            console.log(e)
        }
    });
}

function PythonVersion() {
    const format = {
        label: 'Python',  // (Optional) Badge label
        message: '3.12 | 3.13 | 3.14',  // (Required) Badge message
        labelColor: '#555',  // (Optional) Label color
        color: 'rgb(17, 86, 204)',  // (Optional) Message color
    }
    const badgeString = makeBadge(format);
    fs.writeFile("python.svg", badgeString, e => {
        if (e != null) {
            console.log(e)
        }
    });
}

function PackageManager(){
    const format = {
        label: "Package Repositories",
        message: "PyPI | conda-forge",
        labelColor: "#555",
        color: "rgb(17, 86, 204)"
    }
    const badgeString = makeBadge(format);
    fs.writeFile("package.svg", badgeString, e => {
        if(e != null){
            console.log(e)
        }
    })
}

SPEC0()
PythonVersion()
PackageManager();