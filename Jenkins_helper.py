import jenkins, os, argparse, json

class Jenkins_Helper:
    def __init__(self,args):
        """
        Initialize the Jenkins_Helper class with the Jenkins server URL, JENKINS_USERNAME, JENKINS_PASSWORD, and FILE_NAME
        Args:
            args (argparse.ArgumentParser): The arguments to initialize the Jenkins_Helper class with.
            --JENKINS_URL (str): The Jenkins server URL. Default is "http://jenkins.demo.supersqa.com".
            --JENKINS_USERNAME (str): The Jenkins server JENKINS_USERNAME. Default is "admin".
            --JENKINS_PASSWORD (str): The Jenkins server JENKINS_PASSWORD. Default is "admin".
            --FILE_NAME (str): The Jenkins data file name. Default is "jenkins_data.json".
            --BUILD_DEPTH (int): The number of builds to backup or restore. Default is 3.
        """
        #==============================================================
        #==============================================================
        self.JENKINS_URL = args.JENKINS_URL
        self.JENKINS_USERNAME = args.JENKINS_USERNAME
        self.JENKINS_PASSWORD = args.JENKINS_PASSWORD
        self.file_name = args.FILE_NAME
        self.BUILD_DEPTH = args.BUILD_DEPTH
        #==============================================================
        #==============================================================
        curent_path = os.path.dirname(os.path.realpath(__file__))
        self.file_path = os.path.join(curent_path, "jenkins_data")
        os.makedirs(self.file_path, exist_ok=True)
        self.file_name = os.path.join(self.file_path, self.file_name)
        #============================================================== 
        #==============================================================  
        if self.JENKINS_USERNAME is None or self.JENKINS_PASSWORD is None:
            self.server = jenkins.Jenkins(url=self.JENKINS_URL, timeout=60)
            if self.server.get_whoami() is None:
                raise Exception("Failed to connect to Jenkins server")
            else:
                JENKINS_USERNAME = os.getenv('JENKINS_USERNAME')
                JENKINS_PASSWORD = os.getenv('JENKINS_PASSWORD')
                if JENKINS_USERNAME is None or JENKINS_PASSWORD is None:
                    self.server = jenkins.Jenkins(url=self.JENKINS_URL, timeout=60)
                    if self.server.get_whoami() is None:    
                        raise Exception("Failed to connect to Jenkins server")
                    else:
                        print("Connected to Jenkins server successfully")        
        #==============================================================
        #==============================================================
        if self.JENKINS_USERNAME is not None and self.JENKINS_PASSWORD is not None:
            self.server = jenkins.Jenkins(url=self.JENKINS_URL, username=self.JENKINS_USERNAME, password=self.JENKINS_PASSWORD, timeout=60)
            if self.server.get_whoami() is None:
                raise Exception("Failed to connect to Jenkins server")
            else:
                print("Connected to Jenkins server successfully")
        #==============================================================
        #==============================================================
        
    def get_xml(self, path, type="Job"):
        """
        Get the XML data of a path
        
        Args:
            path (str): The path to get the XML data of.
            
        Returns:
            str: The XML data of the path.
        """
        file_path = os.path.join(self.file_path, "jenkins_data", type)
        file_name = os.path.join(file_path, path+"_config.xml")
        
        with open(file_name, 'r') as file:
            data = file.read()
        return data
    
    def save_xml(self, data, path, type="Job"):
        """
        Save an XML file to a path
        
        Args:
            data (str): The XML data to save.
            path (str): The path to save the XML data to.
        """
        
        file_path = os.path.join(self.file_path, type)
        os.makedirs(file_path, exist_ok=True)
        file_name = os.path.join(file_path, path+"_config.xml")
        print(f"Saving {file_name} ... ", "Type: ", type)
        
        with open(file_name, 'w') as file:
            file.write(data)
    
    def get_job_info(self, job_name):
        """
        Get the information of a job by its name

        Args:
            job_name (str): The name of the job to get the information of.

        Returns:
            dict: The information of the job.
        """
        return self.server.get_job_info(name=job_name)
    
    def get_jobs_by_view(self, view_name):
        """
        Get the jobs of a view by its name

        Args:
            view_name (str): The name of the view to get the jobs of.

        Returns:
            list: The jobs of the view.
        """
        return self.server.get_jobs(view_name=view_name)
    
    def get_job_config(self, job_name):
        """
        Get the configuration of a job by its name (XML format)

        Args:
            job_name (str): The name of the job to get the configuration of.

        Returns:
            str: The configuration of the job in XML format.
        """
        try:
            return self.server.get_job_config(name=job_name)
        except Exception as e:
            return jenkins.EMPTY_CONFIG_XML
        
    def create_job(self, job_name, config):
        """
        Create a job with a name and configuration

        Args:
            job_name (str): The name of the job to create.
            config (str): The configuration of the job in XML format.

        Returns:
            bool: True if the job was created successfully, False otherwise.
        """
        try:
            return self.server.create_job(name=job_name, config_xml=config)
        except Exception as e:
            if "already exists" in str(e):
                self.update_job(job_name, config)
            else:
                return False
            
    def get_queue_info(self):
        """
        Get the information of the Jenkins queued jobs

        Returns:
            dict: The information of the Jenkins queue.
        """
        return self.server.get_queue_info()
    
    def cancel_queue_item(self, queue_id):
        """
        Cancel a queued job by its ID
        
        Args:
            queue_id (int): The ID of the queued job to cancel.
            
        Returns:
            bool: True if the queued job was canceled successfully, False otherwise.
        """
        return self.server.cancel_queue(queue_id=queue_id)
    
    def update_job(self, job_name, config):
        """
        Update a job with a name and configuration

        Args:
            job_name (str): The name of the job to update.
            config (str): The configuration of the job in XML format.

        Returns:
            bool: True if the job was updated successfully, False otherwise.
        """
        return self.server.reconfig_job(name=job_name, config_xml=config)
    
    def copy_job(self, job_name, new_job_name):
        """
        Copy a job with a name to a new job with a new name

        Args:
            job_name (str): The name of the job to copy.
            new_job_name (str): The name of the new job to create.

        Returns:
            bool: True if the job was copied successfully, False otherwise.
        """
        return self.server.copy_job(from_name=job_name, to_name=new_job_name)
    
    def delete_job(self, job_name):
        """
        Delete a job by its name

        Args:
            job_name (str): The name of the job to delete.

        Returns:
            bool: True if the job was deleted successfully, False otherwise.
        """
        return self.server.delete_job(name=job_name)
    
    def enable_job(self, job_name):
        """
        Enable a job by its name (if it is disabled)

        Args:
            job_name (str): The name of the job to enable.

        Returns:
            bool: True if the job was enabled successfully, False otherwise.
        """
        return self.server.enable_job(name=job_name)
    
    def disable_job(self, job_name):
        """
        Disable a job by its name (if it is enabled)

        Args:
            job_name (str): The name of the job to disable.

        Returns:
            bool: True if the job was disabled successfully, False otherwise.
        """
        return self.server.disable_job(name=job_name)
    
    def build_job(self, job_name, parameters=None):
        """
        Build a job by its name with optional parameters (if any)

        Args:
            job_name (str): The name of the job to build.
            parameters (dict, optional): The parameters to pass to the job. Defaults to None.

        Returns:
            bool: True if the job was built successfully, False otherwise.
        """
        try:
            return self.server.build_job(name=job_name, parameters=parameters)
        except Exception as e:
            "already exists" in str(e)
            return "Job already exists"
    
    def get_build_stage(self, job_name, build_number):
        """
        Get the stage of a build by its job name and build number 

        Args:
            job_name (str): The name of the job to get the build stage of.
            build_number (int): The number of the build to get the stage of.

        Returns:
            str: The stage of the build.
        """
        return self.server.get_build_stages(name=job_name, number=build_number)
    
    def get_job_builds(self, job_name):
        """
        Get the builds of a job by its name (all builds)

        Args:
            job_name (str): The name of the job to get the builds of.

        Returns:
            list: The builds of the job.
        """
        try:
            return self.server.get_job_info(name=job_name)['builds']
        except Exception as e:
            return []
            
    def get_job_builds_count(self, job_name):
        return len(self.get_job_builds(job_name=job_name))
    
    def get_build_info(self, job_name, build_number):
        """
        Get the information of a build by its job name and build number

        Args:
            job_name (str): The name of the job to get the build information of.
            build_number (int): The number of the build to get the information of.

        Returns:
            dict: The information of the build.
        """
        return self.server.get_build_info(name=job_name, number=build_number)
    
    def get_job_last_build(self, job_name):
        """
        Get the last build of a job

        Args:
            job_name (str): The name of the job to get the last build of.

        Returns:
            dict: The last build of the job.
        """
        return self.server.get_job_info(name=job_name)['lastBuild']
    
    def get_job_last_build_number(self, job_name, build="lastCompletedBuild"):
        """
        Get the last build number of a job

        Args:
            job_name (str):  The name of the job to get the last build number of.
            
            build (str, optional): The type of build to get the number of [lastBuild, lastCompletedBuild, lastFailedBuild, lastStableBuild, lastSuccessfulBuild, lastUnstableBuild, lastUnsuccessfulBuild]. Defaults to "lastCompletedBuild". 
    
        Returns:
            int: The last build number of the job.
        """
        try:
            return self.server.get_job_info(name=job_name)[build]['number']
        except Exception as e:
            return 0
        
    def get_build_console_output(self, job_name, build_number):
        """
        Get the console output of a build by its job name and build number

        Args:
            job_name (str): The name of the job to get the build console output of.
            build_number (int): The number of the build to get the console output of.

        Returns:
            str: The console output of the build.
        """
        try:
            return self.server.get_build_console_output(name=job_name, number=build_number)
        except Exception as e:
            return ""
        
    def get_build_test_report(self, job_name, build_number):
        """
        Get the test report of a build by its job name and build number

        Args:
            job_name (str): The name of the job to get the build test report of.
            build_number (int): The number of the build to get the test report of.

        Returns:
            dict: The test report of the build.
        """
        try:
            return self.server.get_build_test_report(name=job_name, number=build_number)
        except Exception as e:
            return {}
        
    def get_build_changeset(self, job_name, build_number):
        """
        Get the changeset of a build by its job name and build number (all changes)

        Args:
            job_name (str): The name of the job to get the build changeset of.
            build_number (int): The number of the build to get the changeset of.

        Returns:
            list: The changeset of the build.
        """
        try:
            return self.server.get_build_info(name=job_name, number=build_number)['changeSet']['items']
        except Exception as e:
            return []
    
    def update_next_build_number(self, job_name, next_build_number):
        """
        Update the next build number of a job

        Args:
            job_name (str): The name of the job to update the next build number of.
            next_build_number (int): The next build number to set.

        Returns:
            bool: True if the next build number was updated successfully, False otherwise.
        """
        return self.server.set_next_build_number(name=job_name, number=next_build_number)
    
    def get_build_artifacts(self, job_name, build_number):
        """
        Get the artifacts of a build by its job name and build number (all artifacts)

        Args:
            job_name (str): The name of the job to get the build artifacts of.
            build_number (int): The number of the build to get the artifacts of.

        Returns:
            list: The artifacts of the build.
        """
        try:
            return self.server.get_build_info(name=job_name, number=build_number)['artifacts']
        except Exception as e:
            return []
        
    def get_view_info(self, view_name):
        """
        Get the information of a view by its name
        
        Args:
            view_name (str): The name of the view to get the information of.
            
        Returns:
            dict: The information of the view.
        """
        return self.server.view_exists(name=view_name)
    
    def create_view(self, view_name, view_config = None):
        """
        Create a view with a name
        
        Args:
            view_name (str): The name of the view to create.
            view_config (str, optional): The configuration of the view in XML format. Defaults to None.
            
        Returns:
            bool: True if the view was created successfully, False otherwise.
        """
        if view_config is None:
            view_config = jenkins.EMPTY_VIEW_CONFIG_XML
        try:
            return self.server.create_view(name=view_name, config_xml=view_config)
        except Exception as e:
            if "already exists" in str(e):
                self.update_view(view_name, view_config)
            else:
                return False
            
    def update_view(self, view_name, view_config):
        """
        Update a view with a name and configuration
        
        Args:
            view_name (str): The name of the view to update.
            view_config (str): The configuration of the view in XML format.
            
        Returns:
            bool: True if the view was updated successfully, False otherwise.
        """
        return self.server.reconfig_view(name=view_name, config_xml=view_config)
    
    def delete_view(self, view_name):
        """
        Delete a view by its name
        
        Args:
            view_name (str): The name of the view to delete.
            
        Returns:
            bool: True if the view was deleted successfully, False otherwise.
        """
        return self.server.delete_view(name=view_name)
    
    def get_view_config(self, view_name):
        """
        Get the configuration of a view by its name (XML format)
        
        Args:
            view_name (str): The name of the view to get the configuration of.
            
        Returns:
            str: The configuration of the view in XML format.
        """
        try:    
            self.save_xml(self.server.get_view_config(name=view_name), view_name, "view")
            return self.server.get_view_config(name=view_name)
        except Exception as e:
            self.save_xml(jenkins.EMPTY_VIEW_CONFIG_XML, view_name, "view")
            return jenkins.EMPTY_VIEW_CONFIG_XML
        
    def get_plugin_info(self, plugin_name):
        """
        Get the information of a plugin by its name

        Args:
            plugin_name (str): The name of the plugin to get the information of.

        Returns:
            dict: The information of the plugin.
        """
        return self.server.get_plugin_info(name=plugin_name)
    
    def get_plugin_version(self, plugin_name):
        """
        Get the version of a plugin by its name

        Args:
            plugin_name (str): The name of the plugin to get the version of.

        Returns:
            str: The version of the plugin.
        """
        return self.server.get_plugin_info(name=plugin_name)['version']
    
    def install_plugin(self, plugin_name):
        """
        Install a plugin by its name

        Args:
            plugin_name (str): The name of the plugin to install.

        Returns:
            bool: True if the plugin was installed successfully, False otherwise.
        """
        try:
            return self.server.install_plugin(name=plugin_name)
        except Exception as e:
            if "already exists" in str(e):
                return True
            else:
                return False
            
    def get_node_info(self, node_name):
        """
        Get the information of a node by its name

        Args:
            node_name (str): The name of the node to get the information of.

        Returns:
            dict: The information of the node.
        """
        return self.server.get_node_info(name=node_name)
    
    def get_all_nodes(self):
        """
        Get the information of all nodes

        Returns:
            list: The information of all nodes.
        """
        return self.server.get_nodes()
    
    def get_node_config(self, node_name):
        """
        Get the configuration of a node by its name (XML format)

        Args:
            node_name (str): The name of the node to get the configuration of.

        Returns:
            str: The configuration of the node in XML format.
        """
        try:
            self.save_xml(self.server.get_node_config(name=node_name), node_name, "node")
            return self.server.get_node_config(name=node_name)
        except Exception as e:
            self.save_xml(jenkins.EMPTY_CONFIG_XML, node_name, "node")
            return jenkins.EMPTY_CONFIG_XML
    
    def create_node(self, node_name, config):
        """
        Create a node with a name and configuration

        Args:
            node_name (str): The name of the node to create.
            config (str): The configuration of the node in XML format.

        Returns:
            bool: True if the node was created successfully, False otherwise.
        """
        try:
            return self.server.create_node(name=node_name, config_xml=config)
        except:
            if "already exists" in str(e):
                self.update_node(node_name, config)
            else:
                return False
        
    def update_node(self, node_name, config):
        """
        Update a node with a name and configuration

        Args:
            node_name (str): The name of the node to update.
            config (str): The configuration of the node in XML format.

        Returns:
            bool: True if the node was updated successfully, False otherwise.
        """
        return self.server.reconfig_node(name=node_name, config_xml=config)
    
    def delete_node(self, node_name):
        """
        Delete a node by its name

        Args:
            node_name (str): The name of the node to delete.

        Returns:
            bool: True if the node was deleted successfully, False otherwise.
        """
        return self.server.delete_node(name=node_name)
    
    def enable_node(self, node_name):
        """
        Enable a node by its name (if it is disabled)

        Args:
            node_name (str): The name of the node to enable.

        Returns:
            bool: True if the node was enabled successfully, False otherwise.
        """
        return self.server.enable_node(name=node_name)
    
    def disable_node(self, node_name):
        """
        Disable a node by its name (if it is enabled)

        Args:
            node_name (str): The name of the node to disable.

        Returns:
            bool: True if the node was disabled successfully, False otherwise.
        """
        return self.server.disable_node(name=node_name)
    
    def get_folder_info(self, folder_name):
        """
        Get the information of a folder by its name

        Args:
            folder_name (str): The name of the folder to get the information of.

        Returns:
            dict: The information of the folder.
        """
        return self.server.get_job_info(name=folder_name)
    
    def create_folder(self, folder_name, config=None):
        """
        Create a folder with a name and configuration
        
        Args:
            folder_name (str): The name of the folder to create.
            config (str, optional): The configuration of the folder in XML format. Defaults to None.
            
        Returns:
            bool: True if the folder was created successfully, False otherwise.
        """
        if config is None:
            config = jenkins.EMPTY_FOLDER_XML
        try:
            return self.server.create_job(name=folder_name, config_xml=config)
        except Exception as e:
            if "already exists" in str(e):
                self.update_folder(folder_name, config)
            else:
                return False
            
    def delete_folder(self, folder_name):
        """
        Delete a folder by its name
        
        Args:
            folder_name (str): The name of the folder to delete.
            
        Returns:
            bool: True if the folder was deleted successfully, False otherwise.
        """
        return self.server.delete_job(name=folder_name)
    
    def copy_folder(self, folder_name, new_folder_name):
        """
        Copy a folder with a name to a new folder with a new name

        Args:
            folder_name (str): The name of the folder to copy.
            new_folder_name (str): The name of the new folder to create.

        Returns:
            bool: True if the folder was copied successfully, False otherwise.
        """
        return self.server.copy_job(from_name=folder_name, to_name=new_folder_name)
    
    def get_folder_config(self, folder_name):
        """
        Get the configuration of a folder by its name (XML format)

        Args:
            folder_name (str): The name of the folder to get the configuration of.

        Returns:
            str: The configuration of the folder in XML format.
        """
        return self.server.get_job_config(name=folder_name)
    
    def get_promotions(self, promo_job_name):
        """
        Get the promotions of a job by its name
        
        Args:
            promo_job_name (str): The name of the job to get the promotions of.
            
        Returns:
            list: The promotions of the job.
        """
        return self.server.get_promotions(name=promo_job_name)
    
    def create_promotion(self, promo_job_name, promotion_name, promotion_config = None):
        """
        Create a promotion with a name and configuration
        
        Args:
            promo_job_name (str): The name of the job to create the promotion for.
            promotion_name (str): The name of the promotion to create.
            promotion_config (str, optional): The configuration of the promotion in XML format. Defaults to None.
            
        Returns:
            bool: True if the promotion was created successfully, False otherwise.
        """
        if promotion_config is None:
            promotion_config = jenkins.EMPTY_PROMO_CONFIG_XML
        return self.server.create_promotion(name=promo_job_name, promotion_name=promotion_name, config_xml=promotion_config)
    
    def check_promotion_exists(self, promo_job_name, promotion_name):
        """
        Check if a promotion exists for a job by its name
        
        Args:
            promo_job_name (str): The name of the job to check the promotion for.
            promotion_name (str): The name of the promotion to check.
            
        Returns:
            bool: True if the promotion exists, False otherwise.
        """
        return self.server.promotion_exists(name=promo_job_name, promotion_name=promotion_name)
    
    def get_promotion_config(self, promo_job_name, promotion_name):
        """
        Get the configuration of a promotion by its name (XML format)
        
        Args:
            promo_job_name (str): The name of the job to get the promotion configuration of.
            promotion_name (str): The name of the promotion to get the configuration of.
            
        Returns:
            str: The configuration of the promotion in XML format.
        """
        try:
            self.save_xml(self.server.get_promotion_config(name=promo_job_name, promotion_name=promotion_name), promo_job_name, "promotion")
            return self.server.get_promotion_config(name=promo_job_name, promotion_name=promotion_name)
        except Exception as e:
            self.save_xml(jenkins.EMPTY_PROMO_CONFIG_XML, promo_job_name, "promotion")
            return jenkins.EMPTY_PROMO_CONFIG_XML
    
    def reconfig_promotion(self, promo_job_name, promotion_name, promotion_config = None):
        """
        Update a promotion with a name and configuration 
        
        Args:
            promo_job_name (str): The name of the job to update the promotion for.
            promotion_name (str): The name of the promotion to update.
            promotion_config (str, optional): The configuration of the promotion in XML format. Defaults to None.
            
        Returns:
            bool: True if the promotion was updated successfully, False otherwise.
        """
        if promotion_config is None:
            promotion_config = jenkins.PROMO_RECONFIG_XML
        return self.server.reconfig_promotion(name=promo_job_name, promotion_name=promotion_name, config_xml=promotion_config)
    
    def delete_promotion(self, promo_job_name, promotion_name):
        """
        Delete a promotion by its name
        
        Args:
            promo_job_name (str): The name of the job to delete the promotion for.
            promotion_name (str): The name of the promotion to delete.
            
        Returns:
            bool: True if the promotion was deleted successfully, False otherwise.
        """
        return self.server.delete_promotion(name=promo_job_name, promotion_name=promotion_name)
    
    def save_jenkins_data(self):
        """
        Save all Jenkins data to a JSON file
        
        Args:
            None
        """
        data = {}
        print("Saving Jobs Info ...")
        data['jobs'] = self.server.get_jobs()
        for job in data['jobs']:   
            self.save_xml(self.get_job_config(job['name']), job['name'], "Job")
            
            job['builds'] = self.get_job_builds(job['name'])
            for build in job['builds']:
                print(f"Saving {job['name']} {build['number']} Info ...")
                build['info'] = self.get_build_info(job['name'], build['number'])
                build['console_output'] = self.get_build_console_output(job['name'], build['number'])
                build['test_report'] = self.get_build_test_report(job['name'], build['number'])
                build['changeset'] = self.get_build_changeset(job['name'], build['number'])
                build['artifacts'] = self.get_build_artifacts(job['name'], build['number'])
                if job['builds'].index(build) > self.BUILD_DEPTH:
                    break
                
        print("Saving Views Info ...")
        data['views'] = self.server.get_views()
        for view in data['views']:
            print(f"Saving {view['name']} Info ...")
            self.save_xml(self.get_view_config(view['name']), view['name'], "View")
        
        print("Saving Plugins Info ...")
        plugins = self.server.get_plugins()
        data['plugins'] = []
        print(f"Saving {len(plugins)} Plugins Info ..." )

        for key, plugin in plugins.items():
            print(f"Saving {plugin['shortName']} Info ...")
            data['plugins'].append(plugin)
            
        print("Saving Nodes Info ...")
        data['nodes'] = self.server.get_nodes()
        for node in data['nodes']:
            print(f"Saving {node['name']} Info ...")
            self.save_xml(self.get_node_config(node['name']), node['name'], "Node")
        
        with open(self.file_name, 'w') as file:
            json.dump(data, file)
   
        print("Jenkins data saved successfully")
    
    def restore_jenkins_data(self):
        """
        Restore all Jenkins data from a JSON file
        
        Args:
            None
        """
        with open(self.file_name, 'r') as file:
            data = json.load(file)

        print("Restoring Jobs Info ...")
        jobs = data['jobs']
        for job in jobs:
            print(f"Restoring {job['name']} Info ...")
            self.create_job(job['name'], self.get_xml(job['name'], "Job"))
            for build in job['builds']:
                print(f"Restoring {job['name']} {build['number']} Info ...")
                self.build_job(job['name'],build)
                if job['builds'].index(build) > self.BUILD_DEPTH:
                    break
                
        print("Restoring Views Info ...")
        views = data['views']
        for view in views:
            print(f"Restoring {view['name']} Info ...")
            self.create_view(view['name'], self.get_xml(view['name'], "View"))
            
        print("Restoring Plugins Info ...")
        plugins = data['plugins']
        print(f"Restoring {len(plugins)} Plugins Info ..." )
        for plugin in plugins:
            print(f"Restoring {plugin['shortName']} Info ...")
            self.install_plugin(plugin['shortName'])
            
        print("Restoring Nodes Info ...")
        nodes = data['nodes']
        for node in nodes:
            print(f"Restoring {node['name']} Info ...")
            self.create_node(node['name'], self.get_xml(node['name'], "Node"))   
        print("Jenkins data restored successfully")
             
if __name__ == '__main__':
    
    args = argparse.ArgumentParser()
    args.add_argument("--JENKINS_URL", help="Jenkins server URL", default="http://jenkins.demo.supersqa.com")
    args.add_argument("--JENKINS_USERNAME", help="Jenkins server JENKINS_USERNAME",default="admin")
    args.add_argument("--JENKINS_PASSWORD", help="Jenkins server JENKINS_PASSWORD",default="admin")
    args.add_argument("--BACKUP", help="Backup Jenkins data", action="store_true", default=True)
    args.add_argument("--RESTORE", help="Restore Jenkins data", action="store_true", default=False)
    args.add_argument("--FILE_NAME", help="Jenkins data file name", default="jenkins_data.json")
    args.add_argument("--BUILD_DEPTH", help="Number of builds to backup or restore", default=3, type=int)
    args = args.parse_args()
    
    jenkins_helper = Jenkins_Helper(args)
    if args.BACKUP:
        jenkins_helper.save_jenkins_data()
    elif args.RESTORE:
        jenkins_helper.restore_jenkins_data()
    