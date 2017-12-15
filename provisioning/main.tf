provider "aws" {
  region = "us-east-1"
}

variable "github_repo" {
  default = ""
}

variable "f_suff" {
  default = ""
}

variable "wdir" {
  default = ""
}

variable "bucket" {
  default = ""
}

resource "aws_iam_role" "codebuild_role" {
  name = "codebuild-role-"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "codebuild_policy" {
  name        = "codebuild-policy"
  path        = "/service-role/"
  description = "Policy used in trust relationship with CodeBuild"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": [
        "*"
      ],
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
    }
  ]
}
POLICY
}

resource "aws_iam_policy_attachment" "codebuild_policy_attachment" {
  name       = "codebuild-policy-attachment"
  policy_arn = "${aws_iam_policy.codebuild_policy.arn}"
  roles      = ["${aws_iam_role.codebuild_role.id}"]
}

resource "aws_codebuild_project" "foo" {
  name          = "to_grey"
  description   = "build docker images with batch workload"
  build_timeout = "5"
  service_role  = "${aws_iam_role.codebuild_role.arn}"

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type    = "BUILD_GENERAL1_SMALL"
    image           = "aws/codebuild/docker:17.09.0"
    type            = "LINUX_CONTAINER"
    privileged_mode = true

    environment_variable {
      "name"  = "F_SUFF"
      "value" = "${var.f_suff}"
    }

    environment_variable {
      "name"  = "WDIR"
      "value" = "${var.wdir}"
    }

    environment_variable {
      "name"  = "BUCKET"
      "value" = "${var.bucket}"
    }
  }

  source {
    type     = "GITHUB"
    location = "${var.github_repo}"
  }

  tags {
    "Environment" = "Test"
  }
}

resource "null_resource" "local" {
  provisioner "local-exec" {
    command = "aws codebuild create-webhook --project-name ${aws_codebuild_project.foo.name}"
  }
}
