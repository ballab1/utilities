#!/usr/bin/env groovy

import groovy.json.*

import java.awt.AttributeValue
import java.text.SimpleDateFormat
import java.util.Map


class RepoEntry {
    String digest
    String createTime
    ArrayList<String> tags = []

    //-------------------------------------
    RepoEntry(Object data) {
        digest = data.digest
        createTime = data.createTime
        tags = data.tags
    }

    //-------------------------------------
    int getNumTags() {
        tags.size()
    }

    //-------------------------------------
    String list(String name) {
        String out = ''
        tags.sort().each { k ->
            out += createTime + '      ' +name + ':' + k.toString() + '\n'
        }
        out
    }

    //-------------------------------------
    String toString() {
        String out = '       ' + digest + ', ' + createTime + '\n'
        tags.sort().each { k ->
            out += '          ' + k.toString() + '\n'
        }
        out
    }
}

class RepoContents {
    String name
    String id
    ArrayList<RepoEntry> digests = []

    //-------------------------------------
    RepoContents(Object data) {
        name = data.repository
        id = data.id
        data.digests.each { x ->
            digests += new RepoEntry(x)
        }
    }

    //-------------------------------------
    int getNumTags() {
        int count = 0
        digests.each { it ->
            count += it.numTags
        }
        return count
    }

    //-------------------------------------
    int getNumImages() {
        digests.size()
    }

    //-------------------------------------
    String list() {
        String out = ''
        digests.sort{it.createTime}.each { k ->
            out += k.list(name)
        }
        if (numImages > 0) {
            out += '\n'
        }
        out
    }

    //-------------------------------------
    String report() {
        String out = this.summary()
        digests.sort{it.createTime}.each { k ->
            out += k.toString() + '\n'
        }
        out
    }

    //-------------------------------------
    String summary() {
        return String.format('%4s: %-37s  Images: %-4s Tags: %3d\n', id, name+',', numImages+',', numTags)
    }
}

class JsonData {
    String base
    ArrayList<RepoContents> repos = []

    //-------------------------------------
    JsonData(String base, String jsonFile) {
        this.base = base

        def jsonFileData = new File(jsonFile)
        if (jsonFileData.exists() && jsonFileData.text) {
            def slurper = new JsonSlurper()
            Map json = slurper.parseText('{"data":'+jsonFileData.text+'}')
            parser(json)
        }
    }

    //-------------------------------------
    private int getNumImages()  {
        int imageCount = 0
        repos.each { r ->
            imageCount += r.numImages
        }
        return imageCount
    }

    //-------------------------------------
    private int getNumRepos() {
        return repos.size()
    }

    //-------------------------------------
    private int getNumTags() {
        int tagCount = 0
        repos.each { r ->
            tagCount += r.numTags
        }
        return tagCount
    }

    //-------------------------------------
    def parser(Map json) {
        json.data.each { k ->
            repos += new RepoContents(k)
        }
    }

    //-------------------------------------
    String report() {
        if (repos.size() == 0) {
            System.err << 'no data found'
        }

        else {
           this.reportSummary()
           this.reportDetails()
           this.reportList()
        }
        ''
    }

    //-------------------------------------
    String reportDetails() {
        def out = this.reportFile('reportDetails.txt')
        out << 'Repository Details:\n\n'
        repos.each { r ->
            out << r.report()
        }
        ''
    }

    //-------------------------------------
    def reportFile(String name) {
        def out = new File("${base}/${name}")
        if ( out.exists() ) {
            out.delete()
        }
        def date = new Date()
        def sdf = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss")
        out <<  '\nDate:  ' + sdf.format(date) + '\n\n'
        out << 'Overview:'
        out << '\nTotal number of repos:  ' + numRepos
        out << '\nTotal number of images: ' + numImages
        out << '\nTotal number of tags:   ' + numTags
        out << '\n\n'
        return out
    }

    //-------------------------------------
    String reportList() {
        def out = this.reportFile('reportList.txt')
        out << 'Image List:\n\n'
        repos.each { r ->
            out << r.list()
        }
        ''
    }

    //-------------------------------------
    String reportSummary() {
        def out = this.reportFile('summary.txt')
        out << 'Summary:\n\n'
        repos.each { r ->
            out << r.summary()
        }
        ''
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//     MAIN
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////

def base = System.getenv('BASE') ?: '/home/groovy/scripts'
def jsonFile = System.getenv('JSON') ?: "${base}/registryReport.json"

def processor = new JsonData(base, jsonFile)
processor.report()
''
